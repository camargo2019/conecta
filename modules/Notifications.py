#!/usr/bin/python3

import os
import sys
import json
from tkinter import *
from PIL import ImageTk, Image

class Notification:
	def __init__(self, title="Conecta IT", subtitle="Oops Error...", descrition="Error[00] - Por favor, Contate o Administrador do sistema!", icone="client_user", wait=0, cancel='False'):
		root = Tk()
		self.root = root
		root.title(title)
		root["borderwidth"] = 0
		w = 450
		h = 180
		ws = root.winfo_screenwidth()
		hs = root.winfo_screenheight()
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		if(wait > 0):
			wait2 = str(wait)+"000"
			root.after(wait2,root.destroy)
		dir_path = "C:\\ConectaIT\\modules"
		root.geometry('%dx%d+%d+%d' % (w, h, x, y))
		root.iconbitmap(dir_path+'\\..\\media\\img\\icone.ico')
		root.resizable(0, 0)
		root.wm_attributes("-topmost", True)
		container = Frame(root)
		container["width"] = w
		container["height"] = 140
		container.pack()
		img = Image.open(dir_path+'\\..\\media\\img\\'+icone+'.png')
		img = img.resize((60,60), Image.ANTIALIAS)
		imagem = ImageTk.PhotoImage(img, master=root)
		labelError = Label(container, image=imagem)
		labelError.pack()

		labelMensagem = Label(container, text=subtitle)
		labelMensagem["font"] = ("Arial", "15", "bold")
		labelMensagem.pack()

		subMensagem = Label(container, text=descrition)
		subMensagem["font"] = ("Arial", "12")
		subMensagem.pack()

		containerOK = Frame(root)
		containerOK.pack(padx=150, pady=10)

		buttonOK = Button(containerOK, text="OK", command=self.setvalue)
		buttonOK["width"] = 5
		buttonOK["background"] = "white"
		buttonOK.pack(side=LEFT)
		self.returnValue = False

		if(cancel == 'True'):
			buttonCancelar = Button(containerOK, text="Cancelar", command=self.nonevalue)
			buttonCancelar["width"] = 6
			buttonCancelar["background"] = "white"
			buttonCancelar.pack(side=LEFT, padx=5)

		root.mainloop()

	def setvalue(self):
		self.returnValue = True
		self.root.destroy()

	def nonevalue(self):
		self.returnValue = False
		self.root.destroy()