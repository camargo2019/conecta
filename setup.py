#!/usr/bin/python3

import os
import sys
import json
from tkinter import *
import psutil
import subprocess
pid = os.getpid()
for proc in psutil.process_iter(['pid', 'name']):
    inf = json.dumps(proc.info)
    inf2 = json.loads(inf)
    if(inf2['name'] == 'ConectaIT.exe' and inf2['pid'] != pid):
        subprocess.call('taskkill /F /PID '+str(inf2['pid']))

from PIL import ImageTk, Image
from modules.Notifications import Notification

dir_path = "C:\\ConectaIT"
tkTelaTemporario = Tk()
tkTelaTemporario.title('ConectaIT')
tkTelaTemporario["borderwidth"] = 0
tkTelaTemporario.resizable(0, 0)
tkTelaTemporario.iconbitmap(dir_path+'\\media\\img\\icone.ico')
tkTelaTemporario.overrideredirect(True)
tkTelaTemporario.bind("<Escape>", lambda e: e.widget.quit())
tkTelaTemporario.focus_set()
wid = 550
hei = 300
ws = tkTelaTemporario.winfo_screenwidth()
hs = tkTelaTemporario.winfo_screenheight()
tkTelaTemporario.wm_attributes("-topmost", True)
tkTelaTemporario.config(bg='white')
x = (ws/2) - (wid/2)
y = (hs/2) - (hei/2)
tkTelaTemporario.geometry('%dx%d+%d+%d' % (wid, hei, x, y))
img = Image.open(dir_path
                 +'\\media\\img\\logo.png')
img = img.resize((550,300), Image.ANTIALIAS)
tkTelaTemporario.image = ImageTk.PhotoImage(img)
labelTk = Label(tkTelaTemporario, image=tkTelaTemporario.image)
labelTk.config(bg='white')
labelTk.pack()
tkTelaTemporario.after(10000,tkTelaTemporario.destroy)
tkTelaTemporario.mainloop()

from modules.autoupdate import *
from modules.user import *
from modules.logged import *
from modules.database.database import *
from modules.database.datalocal import *
from modules.RequiredInternet import *
from modules.JornadaLogs import *
from media import *

db = DataBase()
"""
ASADMIN = 'asadmin'
if sys.argv[-1] != ASADMIN:
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    try:
    	shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
    except:
    	root = Tk()
    	root.title("ConectaIT - Error")
    	root["borderwidth"] = 0
    	w = 400
    	h = 140
    	ws = root.winfo_screenwidth()
    	hs = root.winfo_screenheight()
    	x = (ws/2) - (w/2)
    	y = (hs/2) - (h/2)BloquearTeclas
    	root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    	root.iconbitmap('media/img/icone.ico')
    	root.resizable(0, 0)
    	container = Frame(root)
    	container["width"] = w
    	container["height"] = h
    	container.pack()
    	img = Image.open('media/img/client_user.png')
    	img = img.resize((60,60), Image.ANTIALIAS)
    	imagem = ImageTk.PhotoImage(img)
    	labelError = Label(container, image=imagem)
    	labelError.pack()

    	labelMensagem = Label(container, text="Oops Error...")
    	labelMensagem["font"] = ("Arial", "15", "bold")
    	labelMensagem.pack()

    	subMensagem = Label(container, text="Error[01] - Por favor, execute o ConectaIT como administrador!")
    	subMensagem["font"] = ("Arial", "12")
    	subMensagem.pack()

    	root.mainloop()
    	quit()
else:"""
    #server = None 
    #logTypes = ["System", "Application", "Security"]
    #event_mouse_and_teclado = Thread(target=getAllEvents(server, logTypes, "C:\\PythonDeve\\conecta"))
    #event_mouse_and_teclado.start()

startRequiredInternet = Thread(target=RequiredInternet)
startRequiredInternet.start()
try:
    dadosInfo = InfoJornadaLogs()
    login0 = VerifcarLogin()
    idUser0 = login0.valida()
    validar_senha0 = db.dados_usuario(idUser0)
except:
    dadosInfo = InfoJornadaLogs()
    validar_senha0 = False
if(validar_senha0 != False):
    dbLocal = DataLocal()
    infoDbLocal = dbLocal.dados()
    idUsuario = validar_senha0["employee"]["id"]
    ativoUser = db.ativo_user(idUsuario)
    if(ativoUser != False):
        AutoUpdate()
        TkInit_user()
        dbLocal.limpar_logs()
        sys.exit()
    else:
        FinalizaJornadaLogs()
        dbLocal.remove_id()
        TkInit_Logged()

        dbLocal = DataLocal()
        login = VerifcarLogin()
        idUser = login.valida()
        validar_senha = db.dados_usuario(idUser)
        if (validar_senha != False):
            AutoUpdate()
            TkInit_user()
        dbLocal.limpar_logs()
        sys.exit()
else:
    FinalizaJornadaLogs()
    TkInit_Logged()

    dbLocal = DataLocal()
    login = VerifcarLogin()
    idUser = login.valida()
    validar_senha = db.dados_usuario(idUser)
    if(validar_senha != False):
        AutoUpdate()
        TkInit_user()
    dbLocal.limpar_logs()
    sys.exit()
startRequiredInternet.join(1)