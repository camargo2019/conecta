#!/usr/bin/python3
import os
import sys
import time
import json
import socket
import subprocess
import pygetwindow as gw
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread

class RequiredInternet:
	def __init__(self):
		while True:
			host = 'gmail.com'
			a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			a.settimeout(.5)
			try:
				b = a.connect_ex((host, 80))
				a.close()
			except:
				for janela in gw.getWindowsWithTitle('ConectaIT'):
					janela.close()
				for janela2 in gw.getWindowsWithTitle('ConectaIT - Área do Usuário'):
					janela2.close()
				for janela3 in gw.getWindowsWithTitle('ConectaIT - Login'):
					janela3.close()
				for janela4 in gw.getWindowsWithTitle('Conecta'):
					janela4.close()
				root = Tk()
				root.title("ConectaIT - Error Internet")
				root["borderwidth"] = 0
				w = 400
				h = 160
				ws = root.winfo_screenwidth()
				hs = root.winfo_screenheight()
				x = (ws/2) - (w/2)
				y = (hs/2) - (h/2)
				root.geometry('%dx%d+%d+%d' % (w, h, x, y))
				root.iconbitmap('C:\\ConectaIT\\media\\img\\icone.ico')
				root.wm_attributes("-topmost", True)
				root.resizable(0, 0)
				container = Frame(root)
				container["width"] = w
				container["height"] = h
				container.pack()
				img = Image.open('C:\\ConectaIT\\media\\img\\network.png')
				img = img.resize((60,60), Image.ANTIALIAS)
				imagem = ImageTk.PhotoImage(img, master=root)
				labelError = Label(container, image=imagem)
				labelError.pack()

				labelMensagem = Label(container, text="Ops Error...")
				labelMensagem["font"] = ("Arial", "15", "bold")
				labelMensagem.pack()
				subMensagem = Label(container, text="Você precisa estar conectado(a) com a internet!")
				subMensagem["font"] = ("Arial", "12")
				subMensagem.pack()

				containerOK = Frame(root)
				containerOK.pack(padx=0, pady=10)

				buttonOK = Button(containerOK, text="OK", command=root.destroy)
				buttonOK["width"] = 15
				buttonOK["background"] = "white"
				buttonOK.pack()
				root.mainloop()
				while True:
					try:
						b = a.connect_ex((host, 80))
						a.close()

						subprocess.call(['C:\\ConectaIT\\ConectaIT.exe'])

					except:
						pass
				#subprocess.call(['taskkill /IM ConectaIT.exe'])
				sys.exit()
			time.sleep(30)