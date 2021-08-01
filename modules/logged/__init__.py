#!/usr/bin/python3

import os
import sys
import json
from tkinter import *
from PIL import ImageTk, Image
from ..database.database import *

db = DataBase()
definitions = {
    '9': '[0-9]',
    'a': '[a-zA-Z]',
    'x': '[a-zA-z0-9]'
}

class MaskedWidget(Entry):
    def __init__(self, master, format_type, **kw):
        self.fields = {
            'type': format_type,
            'mask': None,
            'monetary': False,
            'dec_places': 2,
            'dec_sep': '.',
            'tho_places': 3,
            'tho_sep': ',',
            'symbol': '',
            'fmt_neg': '-%(symbol)s%(amount)s',
            'fmt_pos': '%(symbol)s%(amount)s',
            'placeholder': '_',
            'textvariable': None,
        }

        if str(format_type).lower() == 'fixed':
            assert 'mask' in kw, 'the fixed mask, is not present'

        self.fields['mask'] = kw.pop('mask', '').lower()
        for k in list(kw.keys()):
            if k in self.fields:
                if k!='textvariable':
                    self.fields[k]=kw.pop(k)
                else:
                    self.fields[k]=kw[k]
        if not 'textvariable' in kw:
            self.fields['textvariable']=StringVar(master)
            kw['textvariable'] = self.fields['textvariable']
        Entry.__init__(self, master, **kw)

        self.defs = definitions
        self.tests = []
        self.partialPosition = None
        self.firstNonMaskPosition = None
        self.len = len(self.fields['mask'])
        for i,c in enumerate(self.fields['mask'].lower()):
            if c == '?':
                self.len -= 1
                self.partialPosition = i
            atom = self.defs.get(c, None)
            self.tests.append(re.compile('(%s)'%atom) if atom else atom)
            if not atom and self.firstNonMaskPosition==None:
                self.firstNonMaskPosition = len(self.tests)-1

        self.writeBuffer()

        if str(self.cget("state")).upper()!="DISABLED":
            self.bind('<KeyPress>', self._onKeyPress, True)
            self.bind('<KeyRelease>', lambda e: 'break', True)
            self.bind('<FocusIn>', self._onFocusIn, True)

    def clean_numeric(self, string):
        if not isinstance(string, basestring): string = str(string)
        string = string.replace(self.fields['symbol']+' ', '')\
                       .replace(self.fields['tho_sep'], '')\
                       .replace(self.fields['dec_sep'], '.')
        if not '.' in string:
            string = list(string)
            string.insert(-2, '.')
            string = ''.join(string)
        return string.partition('.')

    def fmt_numeric( self, amount):
        temp = '00' if not '.' in str(amount) \
                    else str(amount).split('.')[1]
        l = []
        amount = amount.split('.')[0]
        try:
            minus = float(''.join(self.clean_numeric(amount)))<0
        except ValueError:
            minus = 0
        if len(amount)> self.fields['tho_places']:
            nn = amount[-self.fields['tho_places']:]
            l.append(nn)
            amount = amount[:len(amount)-self.fields['tho_places']]
            while len(amount) > self.fields['tho_places']:
                nn = amount[len(amount)-self.fields['tho_places']:]
                l.insert(0, nn)
                amount = amount[0:len(amount)-self.fields['tho_places']]

        if len(''.join(self.clean_numeric(amount)))>0: l.insert(0, amount)
        amount = self.fields['tho_sep'].join(l)+self.fields['dec_sep']+temp
        if minus:
            amount = self.fields['fmt_neg']%{
                'symbol':self.fields['symbol'],
                'amount': amount
            }
        else:
            amount = self.fields['fmt_pos']%{
                'symbol': (self.fields['symbol']+' ') if self.fields['symbol'] else '',
                'amount': amount
            }
        return amount

    def seekNext(self, pos):
        if 0 <= pos+1<self.len:
            if self.tests[pos+1]:
                return pos+1
            return self.seekNext(pos+1)
        return pos

    def seekPrev(self, pos):
        if 0 <= pos-1 < self.len:
            if self.tests[pos-1]:
                return pos-1
            return self.seekPrev(pos-1)
        return pos

    def shiftL(self, begin, end):
        if begin < 0: return
        for i in range(self.len):
            j = self.seekNext(begin)
            if self.tests[i]:
                if j < self.len and self.tests[i].match(self.buffer[i]):
                    self.buffer[i] = self.buffer[j]
                    self.buffer[j] = self.fields['placeholder']
                else:
                    break

    def shiftR(self, pos, c):
        if pos in range(len(self.len)):
            j = self.seekNext(pos)
            t = self.buffer[pos]
            if not t == c and j < self.len and t == self.fields['placeholder']:
                self.buffer[pos] = c

    def writeBuffer(self):
        self.fields['textvariable'].set(
            ''.join(
                filter(
                    lambda x: x!=None,
                        map(
                            lambda c, self=self:
                                (self.fields['placeholder']
                                if self.defs.get(c, None)
                        else c)
                    if c!='?' else None, self.fields['mask'])
                )
            )
        )
        return self.get()

    def _onFocusIn(self, event):
        if self.len>0 and self.tests[0]:
            self.icursor(0)
        else:
            self.icursor(self.seekNext(0))

    def _onKeyPress(self, event):
        if event.keysym == 'Tab':
            return
        elif event.keysym == 'Escape':
            if self.fields['type'] == 'fixed':
                self.writeBuffer()
            else:
                self.delete(0, len(event.widget.get()))
        widget = event.widget
        val = widget.get()
        idx = widget.index(INSERT)

        if event.keysym == 'Left':
            if 0 <= idx < self.len:
                if idx < self.firstNonMaskPosition:
                    return 'break'
                elif not self.tests[idx]:
                    widget.icursor(self.seekPrev(idx))
        elif event.keysym == 'Right':
            if 0 <= idx < self.len:
                if idx >= self.len:
                    return 'break'
                elif not self.tests[idx]:
                    widget.icursor(self.seekNext(idx))
        elif event.keysym == 'BackSpace' and self.fields['type'] != 'numeric':
            def repl_or_stop(cls, wget, pos):            
                if 0 <= pos <= cls.len:
                    if not cls.tests[pos]:
                        pos = cls.seekPrev(pos)
                    cls._write_char(pos, cls.fields['placeholder'], -1)
                return 'break'
            repl_or_stop(self, widget, idx - 1)
            return 'break'
        else:
            if self.fields['type'] == 'fixed':
                if self._write_char(idx, event.char) == 'break':
                    return 'break'
            elif self.fields['type'] == 'numeric' and event.char.isdigit():
                if val:
                    widget.delete(0, len(val))
                    head, sep, tail = self.clean_numeric(val)
                else:
                    head, sep, tail = '0', '.', '00'

                if not head:
                    head = '0'
                if len(tail) < 2:
                    tail = '0' + tail

                if tail and len(tail + event.char) <= 2 and (int(tail+event.char))<99:
                    tail = tail[1:] + event.char
                else:
                    if not int(head):
                        head = tail[0] if tail else '0'
                    else:
                        head += tail[0]
                    tail = tail[1:] + event.char
                    widget.insert(0, ''.join([head, sep, tail]))
                return 'break'
            elif self.fields['type'] == 'numeric' and event.keysym == 'BackSpace':
                if val:
                    widget.delete(0, len(val))
                    head, sep, tail = self.clean_numeric(val[:-1])
                else:
                    head, sep, tail = '0', '.', '00'
                widget.insert(0, ''.join([head, sep, tail]))
                return 'break'
            else:
                self.bell()
                return 'break'

    def insert(self, index, value):
        if self.fields['type']=='numeric':
            Entry.insert(self, index, self.fmt_numeric(value))
        else:
            for c in str(value):
                while (not self.tests[index] or not self.tests[index].match(c)):
                    index += 1
                self._write_char(index,c)
                index += 1

    def _write_char(self, idx, char, direction=+1):
        if 0<=idx<self.len and self.tests[idx]:
            if char != self.fields['placeholder'] and not self.tests[idx].match(char):
                self.bell()
                return 'break'
            self.delete(idx)
            Entry.insert(self, idx, char)
            if direction == +1:
                if idx + 1 < self.len and not self.tests[idx+1]:
                    idx = self.seekNext(idx)
                else:
                    idx += 1
            elif direction == -1 and \
                idx - 1 >= 0 and \
                not self.tests[idx]:
                idx = self.seekPrev(idx)
            self.icursor(idx)
            return 'break'
        else:
            self.bell()
            return 'break'

class SalvaDadosDB:
	def salvar(self, cpf):
            information = db.ver_dados(cpf)
            #print(info["employee"]["id"])
            dir_path = "C:\\ConectaIT\\modules\\logged"
            arquivo2 = open(dir_path+"\\..\\database\\data\\database.json", "w")
            arquivo2.write(json.dumps(information))
            idUser = information["employee"]["id"]
            arquivo3 = open(dir_path+"\\..\\logs\\data\\"+str(idUser)+".json", "w")
            arquivo3.write(json.dumps(information))
            return True
class VerifcarLogin:
	def valida(self):
		dir_path = "C:\\ConectaIT\\modules\\logged"
		arquivo = open(dir_path+"\\..\\database\\data\\database.json", "r")
		returnlogin = arquivo.read()
		try:
			jsondecode = json.loads(returnlogin)

			if db.login_valida(jsondecode["employee"]["cpf"]):
				return jsondecode["employee"]["cpf"]
			else:
				return False
		except:
			return False
class LoggetTemplete:
	def __init__(self, master=None):
		self.fontPadrao = ("Arial", 10)
		self.master = master
		self.primeiroContainer = Frame(master)
		self.primeiroContainer["pady"] = 10
		self.primeiroContainer["width"] = 250
		self.primeiroContainer["height"] = 120
		self.primeiroContainer.pack()

		img = Image.open("C:\\ConectaIT\\modules\\logged"+'\\..\\..\\media\\img\\logo.png')
		img = img.resize((250,120), Image.ANTIALIAS)

		self.logo = ImageTk.PhotoImage(img, master=master)

		self.logoLabel = Label(self.primeiroContainer, image=self.logo)
		self.logoLabel.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer["padx"] = 10
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer["padx"] = 5
		self.terceiroContainer.pack()

		self.quartoContainer = Frame(master)
		self.quartoContainer["pady"] = 10
		self.quartoContainer.pack()

		self.quintoContainer = Frame(master)
		self.quintoContainer.pack()

		self.labelCPF = Label(self.segundoContainer, text="CPF:", anchor="w", justify=LEFT)
		self.labelCPF["font"] = ("Arial", "10", "bold")
		self.labelCPF.pack(side=LEFT)

		self.cpf = MaskedWidget(self.terceiroContainer, 'fixed', mask='999.999.999-99')
		self.cpf["width"] = 230
		self.cpf.pack()

		self.fundo_autenticar = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__))+'\\..\\..\\media\\img\\button_logar.png').resize((120,55), Image.ANTIALIAS), master=master)

		self.autenticar = Button(self.quartoContainer, image=self.fundo_autenticar)
		self.autenticar["text"] = "Autenticar"
		self.autenticar["font"] = ("Arial", "10")
		self.autenticar["width"] = 120
		self.autenticar["height"] = 55
		self.autenticar["borderwidth"] = 0
		self.autenticar["command"] = self.component_logged
		self.autenticar.pack(side=RIGHT)

		self.fundo_cancelar = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__))+'\\..\\..\\media\\img\\btn_buynow_disable.png').resize((120,55), Image.ANTIALIAS), master=master)
		self.cancelar = Button(self.quartoContainer, image=self.fundo_cancelar)
		self.cancelar["text"] = "Cancelar"
		self.cancelar["font"] = ("Arial", "10")
		self.cancelar["width"] = 120
		self.cancelar["height"] = 55
		self.cancelar["borderwidth"] = 0
		self.cancelar["command"] = master.destroy
		self.cancelar.pack(side=LEFT)

		self.mensagem = Label(self.quintoContainer, text="", font=self.fontPadrao)
		self.mensagem.pack()

	def component_logged(self, event=None):
		cpf = self.cpf.get()
		if cpf:
			#try:
			self.mensagem["text"] = "Validando seu login...."
			info = db.login_valida(cpf)
			if(info == "Sucesso"):
				self.mensagem["text"] = "Logado com sucesso"
				slv = SalvaDadosDB()
				slv.salvar(cpf)
				self.master.destroy()
			else:
				self.mensagem["text"] = info
			#except:
			#	self.mensagem["text"] = "Não conseguimos validar o login!"
		else:
			self.mensagem["text"] = "Coloque o seu CPF!"

class TkInit_Logged:
	def __init__(master=None):
		dir_path = "C:\\ConectaIT\\modules\\logged"
		root = Tk()
		root.title('ConectaIT - Login')
		root["borderwidth"] = 0
		root.resizable(0, 0)
		root.iconbitmap(dir_path+'\\..\\..\\media\\img\\icone.ico')
		root.overrideredirect(True)
		wid = 250
		hei = 300
		ws = root.winfo_screenwidth()
		hs = root.winfo_screenheight()
		root.wm_attributes("-topmost", True)
		x = (ws/2) - (wid/2)
		y = (hs/2) - (hei/2)
		root.geometry('%dx%d+%d+%d' % (wid, hei, x, y))
		LoggetTemplete(root)
		root.mainloop()
