#!/usr/bin/python3

import os
import sys
import json
import time
import requests
from tkinter import *
import urllib.request
from PIL import ImageTk, Image
from ..database.database import *
from ..database.datalocal import *
from ..application.AnimatedGif import *
from threading import Thread
import subprocess

class AutoUpdate:
	def __init__(self):
		self.dir_path = "C:\\ConectaIT\\modules\\autoupdate"
		self.dbLocal = DataLocal()
		self.db = DataBase()
		self.dados = self.dbLocal.dados()

		self.version = open(self.dir_path + "\\..\\application\\version.json", "r")
		self.version_decode = json.loads(self.version.read())
		#print(self.version_decode)
		self.url = self.db.url+"/api/auto/update/"+str(self.dados["employee"]["id"])
		self.x = requests.get(self.url)
		self.decode_at = json.loads(self.x.text)
		if self.decode_at["auto_update"]["version"] != self.version_decode["version"]:
			#Carregamento para fazer o download da versão nova
			root = Tk()
			root.title('ConectaIT - Login')
			root["borderwidth"] = 0
			root["bg"] = "white"
			root.resizable(0, 0)
			root.iconbitmap(self.dir_path+'\\..\\..\\media\\img\\icone.ico')
			root.overrideredirect(True)
			wid = 250
			hei = 330
			ws = root.winfo_screenwidth()
			hs = root.winfo_screenheight()
			#root.wm_attributes("-topmost", True)
			x = (ws/2) - (wid/2)
			y = (hs/2) - (hei/1.8)
			root.geometry('%dx%d+%d+%d' % (wid, hei, x, y))
			ImagemLogoFrame = Frame(root)
			ImagemLogoFrame["width"] = 250
			ImagemLogoFrame["height"] = 90
			ImagemLogoFrame["bg"] = "white"
			ImagemLogoFrame.pack()

			ImagemLoadingFrame = Frame(root)
			ImagemLoadingFrame["width"] = 250
			ImagemLoadingFrame["height"] = 150
			ImagemLoadingFrame["bg"] = "white"
			ImagemLoadingFrame.pack()

			TextLabelLoadingFrame = Frame(root)
			TextLabelLoadingFrame["width"] = 250
			TextLabelLoadingFrame["height"] = 50
			TextLabelLoadingFrame["bg"] = "white"
			TextLabelLoadingFrame.pack()

			img = Image.open('media/img/logo.png')
			img = img.resize((210,90), Image.ANTIALIAS)
			logo = ImageTk.PhotoImage(img, master=root)

			ImagemLogo = Label(ImagemLogoFrame, image=logo)
			ImagemLogo["bg"] = "white"
			ImagemLogo.pack()

			ImagemLoading = AnimatedGif(ImagemLoadingFrame, self.dir_path+'\\..\\..\\media\\img\\loading.gif', 0.02)
			ImagemLoading["bg"] = "white"
			ImagemLoading.pack()
			ImagemLoading.start_thread()

			self.textLoading = "Verificando Atualizações"

			self.TextLabelLoading = Label(TextLabelLoadingFrame, text=self.textLoading)
			self.TextLabelLoading["font"] = ("Tahoma", "14")
			self.TextLabelLoading["bg"] = "white"
			self.TextLabelLoading.pack()
			st = Thread(target=self.init_start)
			st.start()
			root.mainloop()

	def init_start(self):
		self.arquivo = self.update_system()
		print(self.arquivo)
		if self.arquivo != False:
			self.textLoading = "Fazendo Atualização"
			self.TextLabelLoading.text = "Fazendo Atualização"
			st2 = Thread(target=self.init_prog)
			st2.start()
			pid = os.getpid()
			os.system('taskkill /F /IM NotificationConectaIT.exe')
			os.system('taskkill /F /PID '+str(pid))

	def init_prog(self):
		proc = subprocess.Popen(self.dir_path + "\\..\\logs\\update\\" + self.arquivo, shell=True)

	def update_system(self):
		self.url2 = "http://topconecta.com.br/portal"
		self.textLoading = "Fazendo Download..."
		self.TextLabelLoading.text = "Fazendo Download..."
		self.upd_dir = self.decode_at["auto_update"]["file_path"]
		self.upd_file = self.decode_at["auto_update"]["file_name"]
		try:
			urllib.request.urlretrieve(self.url2+self.upd_dir+self.upd_file, self.dir_path+"\\..\\logs\\update\\"+self.upd_file)
			return self.upd_file
		except:
			return False