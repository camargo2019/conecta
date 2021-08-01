#!/usr/bin/python3
import os
import sys
import json
import websocket
import time
import datetime
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
from textwrap3 import wrap
from ..database.datalocal import *
from ..database.database import *

class ChatSocket_C:
    def __init__(self, master, id_from, id_to):
        self.employee_id_from = id_from
        self.employee_id_to = id_to
        self.master = master
        self.API_KEY = "hfjkasdhfkjashdfaçsljf"
        self.ws = websocket.WebSocketApp("ws://34.95.239.34:5000/", on_open=self.ws_open, on_message=self.ws_message)

        self.receive_thread = Thread(target=self.ws_thread)
        self.receive_thread.setDaemon(True)
        self.receive_thread.start()

        time.sleep(5)

        self.msg_json = json.dumps(({"type": "init", "message": {"employee_id_from": self.employee_id_from, "employee_id_to" : self.employee_id_to}}))
        self.ws.send(self.msg_json)

    def ws_thread(self):
        self.ws.run_forever()

    def ws_open(self):
        msg_json = json.dumps({"type": "login", "auth": {"employee_id_from": self.employee_id_from, "params": self.API_KEY}})
        print(msg_json)
        self.ws.send(msg_json)

    def ws_send(self, message):
        self.ws_open()
        msg_json = json.dumps(({"type": "message", "message": {"employee_id_from": self.employee_id_from, "employee_id_to" : self.employee_id_to, "type" : "C", "description": message}}))
        print(msg_json)
        self.ws.send(msg_json)

    def ws_message(self, message):
        msg_json = json.loads(message)
        print(msg_json)
        self.master.receive(msg_json["message"]["is_send_from"], msg_json["message"]["description"], msg_json["message"]["start_date"])

    def ws_init(self):
        msg_json = json.dumps(({"type": "init", "message": {"employee_id_from": self.employee_id_from, "employee_id_to" : self.employee_id_to}}))
        print(msg_json)
        self.ws.send(msg_json)

class ScrollFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = Canvas(self, borderwidth=0, background="#ffffff", width=695, height=380)
        self.viewPort = Frame(self.canvas, width=695, height=380,background="#ffffff")
        self.vsb = Scrollbar(self, orient="vertical", width=16, command=self.canvas.yview)
        
        self.vsb.grid(row=0, column=1, sticky='ns')

        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y") 
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw", tags="self.viewPort")
        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        self.canvas.configure(yscrollcommand=self.vsb.set, scrollregion=self.canvas.bbox('all'))

    def onCanvasConfigure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)


class ChatFrame:
    def send(self, event=None):     
        msg = self.entry_field.get("1.0", END)
        if(msg != ""):
            self.ws_send(msg)
        self.entry_field.delete(1.0, END)

    def receive(self, isfrom, message, date):
        hour = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        message = message
        novaMensagem = ""
        for txtLine in wrap(message, 80):
            novaMensagem += txtLine+"\n"
        novaMensagem += "\n"+hour.strftime("%H:%M - %d/%m/%Y")

        if isfrom == 1:
            self.msg_list_escreve = Label(self.primeiroContainer2.viewPort, text=novaMensagem, width=80, bg="gray96", anchor='ne', justify='right', font=self.fontPadrao).pack(padx=0, pady=3)
        else:
            self.msg_list_escreve = Label(self.primeiroContainer2.viewPort, text=novaMensagem, width=80, bg="gray91", anchor='nw', justify='left', font=self.fontPadrao).pack(padx=0, pady=3)

        self.primeiroContainer2.canvas.yview_moveto(3)
        self.primeiroContainer2.onFrameConfigure()

    def rand_func(self, a, b):
        self.webS = ChatSocket_C(self.master, self.InfoUser["employee"]["id"], b)
        self.ws_send = self.webS.ws_send
        self.send_button["state"] = "normal"

    def __init__(self, master):
        self.InfoUserDBLocal = DataLocal()
        self.InfoUser = self.InfoUserDBLocal.dados()
        self.DataBaseInfo = DataBase()
        self.infoUserHierarchGroup = self.DataBaseInfo.init_workday_chat(self.InfoUser["employee"]["cpf"])



        self.base_dir = "C:\\ConectaIT\\modules\\chat"
        self.dir_path = "C:\\ConectaIT\\modules\\chat"

        self.master = master
        self.fontPadrao = ("Arial", 11)
        self.fontMessage = ("Arial", 10)

        self.Conteiner = Frame(self.master)
        self.Conteiner["height"] = 480
        self.Conteiner["width"] = 300
        self.Conteiner["bg"] = "#FFFFFF"
        self.Conteiner.pack(side=LEFT, anchor="nw")

        self.Conteiner0 = Frame(self.master)
        self.Conteiner0["height"] = 480
        self.Conteiner0["width"] = 5
        self.Conteiner0["bg"] = "#F2F2F2"
        self.Conteiner0.pack(side=LEFT)

        self.Conteiner1 = Frame(self.master)
        self.Conteiner1["height"] = 480
        self.Conteiner1["width"] = 695
        self.Conteiner1["bg"] = "#FFFFFF"
        self.Conteiner1.pack(side=LEFT)

        self.tipodeChat = Frame(self.Conteiner1)
        self.tipodeChat["width"] = 695
        self.tipodeChat["height"] = 2
        self.tipodeChat["bg"] = "snow"
        self.tipodeChat.pack()

        self.UsersON = Frame(self.Conteiner)
        self.UsersON["pady"] = 0
        self.UsersON["width"] = 300
        self.UsersON["height"] = 20
        self.UsersON["bg"] = "#FAFAFA"
        self.UsersON.pack()

        self.Ants = 0
        self.ConteinerInfoBoxUserSelect = {}
        self.UrlLinkImg = {}
        self.ConteinerInfoBoxUserSelectImagem = {}
        self.ConteinerInfoBoxUserSelect2 = {}
        self.textConteinerUser = {}
        #self.ConteinerUserTB = ScrollFrame2(self.Conteiner)
        #self.ConteinerUserTB["pady"] = 0
        #self.ConteinerUserTB["bg"] = "#FAFAFA"
        #self.ConteinerUserTB.pack()

        for jso in self.infoUserHierarchGroup["hierarch_group"]:
            self.ConteinerInfoBoxUserSelect[self.Ants] = Canvas(self.Conteiner, width=300, height=50, borderwidth=0, bg="#FFFFFF")
            self.ConteinerInfoBoxUserSelect[self.Ants].bind("<Button-1>", lambda event, a=jso["name"], b=jso["id"]: self.rand_func(a, b))
            self.ConteinerInfoBoxUserSelect[self.Ants].bind("<Key>", lambda event, a=jso["name"], b=jso["id"]: self.rand_func(a, b))
            self.ConteinerInfoBoxUserSelect[self.Ants].pack()
            self.UrlLinkImg[self.Ants] = ImageTk.PhotoImage(Image.open(self.dir_path + "\\..\\logs\\img\\"+self.InfoUserDBLocal.imagem_user_download_outros(jso["imagem"]["file_path"], jso["imagem"]["file_name"])).resize((40, 40), Image.ANTIALIAS), master=self.master)
            self.ConteinerInfoBoxUserSelectImagem[self.Ants] = self.ConteinerInfoBoxUserSelect[self.Ants].create_image(27, 27, image=self.UrlLinkImg[self.Ants])
            for txtLine in wrap(jso["name"], 20):
                self.textConteinerUser[self.Ants] = txtLine
                break
            self.ConteinerInfoBoxUserSelect[self.Ants].create_text(70, 12, font=("Arial", 11), anchor="nw", text=self.textConteinerUser[self.Ants])
            self.Ants = self.Ants + 1



        self.chatLabel = Label(self.tipodeChat, text="Mensagens: " , bg="gray90", width=695,
                              height=2, anchor="nw", font=self.fontPadrao).pack()

        self.primeiroContainer2 = ScrollFrame(self.Conteiner1)
        self.primeiroContainer2["pady"] = 0
        self.primeiroContainer2["width"] = 695
        self.primeiroContainer2["height"] = 400
        self.primeiroContainer2["bg"] = "snow"
        self.primeiroContainer2.pack()

        self.containerEscrever = Frame(self.Conteiner1)
        self.containerEscrever["pady"] = 0
        self.containerEscrever["width"] = 695
        self.containerEscrever["height"] = 30
        self.containerEscrever.pack()

        self.entry_field = Text(self.containerEscrever, font=('Arial', 12), width=70, height=8)
        self.entry_field.pack(side=LEFT, fill=Y)

        self.icone_send = ImageTk.PhotoImage(Image.open(self.dir_path + "\\..\\..\\modules\\chat\\Send.png").resize((40, 40), Image.ANTIALIAS), master=master)

        self.send_button = Button(self.containerEscrever, text="Enviar", command=self.send)
        self.send_button['image'] = self.icone_send
        self.send_button["width"] = 60
        self.send_button["height"] = 60
        self.send_button["bg"] = "#FFFFFF"
        self.send_button["borderwidth"] = 0
        self.send_button["state"] = "disabled"
        self.send_button.pack(side=RIGHT, fill=BOTH)


class TkInit_chat:
    def __init__(self, id_from, id_to):
        self.chat = Tk()
        self.chat.title("Conecta - Chat")
        self.chat["borderwidth"] = 0
        self.chat["bg"] = "white"
        self.w = 1000
        self.h = 480
        self.ws = self.chat.winfo_screenwidth()
        self.hs = self.chat.winfo_screenheight()
        self.x = (self.ws/2) - (self.w/2)
        self.y = (self.hs/2) - (self.h/2)
        self.chat.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        self.chat.iconbitmap('media/img/icone.ico')
        self.chat.resizable(0, 0)
        self.chat.wm_attributes("-topmost", True)
        self.inf = ChatFrame(self.chat)
        self.chat.mainloop()