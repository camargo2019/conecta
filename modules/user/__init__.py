#!/usr/bin/python3

import os
import sys
import json
import pygetwindow as gw
from tkinter import *
from socket import *
from PIL import ImageTk, Image
from threading import Thread
from ..database.datalocal import *
from ..database.database import *
from ..Notifications import Notification
from ..EventosMouseTeclado import *
from ..GravarEventosMouseTeclado import *
from ..chat import *
from ..ReloadSystem import *
from ..JornadaLogs import *
from datetime import datetime, timedelta
import pygetwindow as gw
import psutil
import subprocess
from ..BloquearTeclas import *
from ..BloqueioProgramas import *

"""
for processo in psutil.process_iter(['pid', 'name']):
    inf = json.dumps(processo.info)
    inf2 = json.loads(inf)
    if(inf2["name"] == "NotificationConectaIT.exe"):
		subprocess.call('taskkill /IM NotificationConectaIT.exe')
		subprocess.call([os.path.dirname(os.path.realpath(__file__)) + '\\..\\..\\NotificationConectaIT.exe'])
"""
class RestartClose:
	def __init__(self, master):
		self.dir_path = "C:\\ConectaIT\\modules\\user"
		self.logs = open(self.dir_path + "\\..\\logs\\OnMouseEvents.json", "w")
		data = datetime.now()
		jsondump = json.dumps({'time': data.strftime('%d/%m/%Y %H:%M'), 'position': '[0, 0]'})
		conteudo = jsondump + "\n"
		self.logs.writelines(conteudo)
		self.logs.close()
		while True:
			self.iniciar(master)
			time.sleep(30)

	def iniciar(self, master):
		self.dir_path = "C:\\ConectaIT\\modules\\user"
		self.db_local = DataLocal()
		self.db = DataBase()
		self.logs = open(self.dir_path + "\\..\\logs\\OnMouseEvents.json")
		self.logs2 = open(self.dir_path + "\\..\\logs\\OnKeyboardEvent.json")
		self.logs_abrir = self.logs.readlines()
		self.logs_abrir2 = self.logs2.readlines()
		self.logs.close()
		self.logs2.close()
		self.logs3 = open(self.dir_path + "\\..\\database\\data\\database.json", "r")
		self.logs_abrir3 = self.logs3.read()
		self.logs3.close()
		self.json_logs = json.loads(self.logs_abrir3)

		self.ler_utimo_logs = json.loads(self.logs_abrir[len(self.logs_abrir) - 1])
		self.ler_utimo_logs2 = json.loads(
		    self.logs_abrir2[len(self.logs_abrir2) - 1])
		self.data_time = datetime.strptime(
		    self.ler_utimo_logs['time'], '%d/%m/%Y %H:%M').strftime('%d%m%Y%H%M')
		self.data_time2 = datetime.strptime(
		    self.ler_utimo_logs2['time'], '%d/%m/%Y %H:%M').strftime('%d%m%Y%H%M')
		self.dataTime50MinAntes = datetime.now() - timedelta(seconds=self.json_logs["company"]["settings"]["time_close_after_end_workday"])
		self.dataTime50MinAntes = self.dataTime50MinAntes.strftime('%d%m%Y%H%M')

		self.dados_info = self.db_local.dados()
		self.dados_start = self.dados_info['my_workday']["0"]['end']['end_time']
		self.date_atual = datetime.now().strftime('%d%m%Y')
		self.data_start_separe = self.dados_start.split(':')
		if(str(self.data_start_separe[0])+str(self.data_start_separe[1]) == "0000"):
			self.date_atual2 = str(self.date_atual)+str('24')+str(self.data_start_separe[1])
		else:
			self.date_atual2 = str(self.date_atual)+str(self.data_start_separe[0]) + str(self.data_start_separe[1])
		self.date_agr = datetime.now().strftime('%d%m%Y%H%M')
		if(int(self.date_agr) > int(self.date_atual2)):
			if(self.data_time and self.dataTime50MinAntes):
				if(self.data_time <= self.dataTime50MinAntes):
					for janela in gw.getWindowsWithTitle('ConectaIT'):
						janela.close()
					for janela2 in gw.getWindowsWithTitle('ConectaIT - Área do Usuário'):
						janela2.close()
					for janela3 in gw.getWindowsWithTitle('ConectaIT - Login'):
						janela3.close()
					for janela4 in gw.getWindowsWithTitle('Conecta'):
						janela4.close()
					Notification(title="ConectaIT", subtitle="Atenção!", descrition="Sua jornada de trabalha está sendo \n encerrada por inatividade.",
								 icone="advertising")
					self.db_local.remove_id()
					subprocess.call('C:\\ConectaIT\\ConectaIT.exe')
					master.destroy()


class NotificationPausas:
	def __init__(self):
		dados_db = DataLocal()
		dados_value = dados_db.dados()
		while True:
			for i in dados_value['my_workday']['workday_interval']:
				for e in i['start']['workday_notifications']:
					try:
						data_start = i['start']['start_time']+':00'
					except:
						data_start = "00:00:00"
					horario_atual = datetime.now().strftime('%H:%M:%S')
					time_10min = '00:00:00'
					formato = '%H:%M:%S'
					time_10 = datetime.strptime(data_start, formato) - datetime.strptime(time_10min, formato)
					time_antesNotifica = datetime.strptime(str(horario_atual), formato) - datetime.strptime(str(time_10), formato)
					# print(time_10min_antesNotifica)
					# print(time_antesNotifica)
					# print(str(horario_atual)+" "+str(time))
					if(str(time_antesNotifica) == '00:00' or str(time_antesNotifica) == '00:00:00' or str(time_antesNotifica) == "0:00:00"):
						Notification(title="ConectaIT", subtitle="Atenção!", descrition=e["notification"]["message"], icone="advertising")
					else:
						time.sleep(0.5)

class UserTemplete:
	def __init__(self, master):
		self.dir_path = "C:\\ConectaIT\\modules\\user"
		self.db = DataBase()
		self.dbLocal = DataLocal()
		self.infoDbLocal = self.dbLocal.dados()
		self.imagem_name = self.dbLocal.imagem_user()
		self.master = master
		# Dados do usuário
		self.cpf_client = self.infoDbLocal['employee']['cpf']
		self.nome_client = self.infoDbLocal['employee']['name']
		self.id_client = self.infoDbLocal['employee']['id']

		self.infoUsuario = Frame(master)
		self.infoUsuario["width"] = 400
		self.infoUsuario.pack(pady=10)

		self.imagemUser = ImageTk.PhotoImage(Image.open(self.dir_path+"\\..\\logs\\img\\"+self.imagem_name).resize((60,60), Image.ANTIALIAS))
		self.boxImagemUser = Label(self.infoUsuario, image=self.imagemUser).pack(side=LEFT, fill=Y, padx=15)

		self.detalhesUser = Frame(self.infoUsuario)
		self.detalhesUser["width"] = 300
		self.detalhesUser.pack(side=RIGHT, fill=BOTH)

		self.nomeUser = Label(self.detalhesUser, text=self.nome_client, anchor='w')
		self.nomeUser["font"] = ('Arial', '12')
		self.nomeUser["width"] = 250
		self.nomeUser.pack(padx=15)

		self.nomeUser = Label(self.detalhesUser,text="CPF: "+self.cpf_client, anchor='w')
		self.nomeUser["font"] = ('Arial', '10')
		self.nomeUser["width"] = 200
		self.nomeUser.pack(padx=15)

		self.jornadaDeTrabalhoContainer = Frame(master)
		self.jornadaDeTrabalhoContainer["width"] = 400
		self.jornadaDeTrabalhoContainer["height"] = 100
		self.jornadaDeTrabalhoContainer["background"] = "#4682B4"
		self.jornadaDeTrabalhoContainer.pack()

		self.textoJornadaTitle = "Jornada de Trabalho - "+self.infoDbLocal['my_workday']["0"]['start']['start_time']+" as "+self.infoDbLocal['my_workday']["0"]['end']['end_time']

		self.jornadaTitle = Label(self.jornadaDeTrabalhoContainer, text=self.textoJornadaTitle)
		self.jornadaTitle["font"] = ('Arial', '10')
		self.jornadaTitle["width"] = 400
		self.jornadaTitle["fg"] = "white"
		self.jornadaTitle["background"] = "#4682B4"
		self.jornadaTitle.pack()
		self.paradasText = "Paradas: "
		self.qntParadas = 0
		for intervalos in self.infoDbLocal['my_workday']["workday_interval"]:
			self.qntParadas = self.qntParadas+1
			self.paradasText += intervalos["start"]["start_time"]+" as "+intervalos["end"]["end_time"]+" \n"
		if self.qntParadas <= 0:
			self.paradasText += "\n Você não possui paradas!"

		self.paradasJornada = Label(self.jornadaDeTrabalhoContainer, text=self.paradasText)
		self.paradasJornada["font"] = ('Arial', '10')
		self.paradasJornada["width"] = 400
		self.paradasJornada["fg"] = "white"
		self.paradasJornada["background"] = "#4682B4"
		self.paradasJornada.pack(padx=5)

		self.containerFuncoes = Frame(master)
		self.containerFuncoes["width"] = 400
		self.containerFuncoes["pady"] = 10
		self.containerFuncoes.pack()

		self.dadosInfo = InfoJornadaLogs()


		self.buttonAbrirChat = Button(self.containerFuncoes, text="Abrir Chat", command=self.abrir_chat)
		self.buttonAbrirChat["width"] = 20
		self.buttonAbrirChat["font"] = ('Arial', '10')
		self.buttonAbrirChat["borderwidth"] = 0
		self.buttonAbrirChat["pady"] = 10
		self.buttonAbrirChat["fg"] = "white"
		self.buttonAbrirChat["bg"] = "#1E90FF"
		self.buttonAbrirChat.pack(side=RIGHT, fill=Y, padx=2)

		self.jsa = Thread(target=self.jornada_start_trabalho)
		self.NotificationPausas = Thread(target=NotificationPausas)
		self.init_ = Thread(target=self.init_system)
		self.initBloqueioProgramas = Thread(target=BloqueioProgramas)
		self.Tecla = Thread(target=BloquearTeclas)

		if (self.dadosInfo.returnA != 'start'):
			self.buttonIniciarJornada = Button(self.containerFuncoes, text="Iniciar Jornada",
											   command=self.inciar_jornada_trabalho)
		else:
			dbLocal0 = DataLocal()
			infoDbLocal0 = dbLocal0.bloquear_teclas()
			if infoDbLocal0['locking_specific_keys'] != False:
				self.Tecla.start()
			IniciaJornadaLogs()
			self.initBloqueioProgramas.start()
			self.jsa.start()
			self.init_.start()
			self.buttonIniciarJornada = Button(self.containerFuncoes, text="Finalizar",
											   command=self.inciar_jornada_trabalho)
		self.buttonIniciarJornada["width"] = 20
		self.buttonIniciarJornada["font"] = ('Arial', '10')
		self.buttonIniciarJornada["borderwidth"] = 0
		self.buttonIniciarJornada["pady"] = 10
		self.buttonIniciarJornada["fg"] = "white"
		self.buttonIniciarJornada["bg"] = "#2F4F4F"
		self.buttonIniciarJornada.pack(side=LEFT, fill=Y, padx=2)

	def abrir_chat(self):
		TkInit_chat(self.id_client, 5)
		#Notification(title="ConectaIT - Error", subtitle="Opss...", descrition="Estamos desenvolvendo o Chat!", icone="advertising")

	def init_system(self):
		try:
			restartClose = Thread(target=RestartClose, args=[self.master])
			restartClose.start()
		except:
			pass

	def inciar_jornada_trabalho(self):
		if(self.buttonIniciarJornada['text'] == "Iniciar Jornada"):
			dbLocal0 = DataLocal()
			infoDbLocal0 = dbLocal0.bloquear_teclas()
			if infoDbLocal0['locking_specific_keys'] != False:
				self.Tecla.start()
			IniciaJornadaLogs()
			self.jsa.start()
			self.init_.start()
			self.initBloqueioProgramas.start()
			Notification(title="ConectaIT", subtitle="Oba...", descrition="Sua Jornada foi iniciada!", icone="advertising")
		elif(self.buttonIniciarJornada['text'] == 'Finalizar'):
			FinalizaJornadaLogs()
			self.db.update_status_end(self.infoDbLocal['employee']['id'])
			self.dbLocal.remove_id()
			self.init_.join(1)
			self.buttonIniciarJornada['text'] = 'Iniciar Jornada'
			self.jsa.join(1)
			dbLocal0 = DataLocal()
			infoDbLocal0 = dbLocal0.bloquear_teclas()
			if infoDbLocal0["locking_specific_keys"] != False:
				self.Tecla.join(1)
			self.initBloqueioProgramas.join(1)
			self.master.destroy()
			ReloadSystem()

	def jornada_start_trabalho(self):
		self.db.update_status(self.infoDbLocal['employee']['id'])
		self.janela = gw.getWindowsWithTitle('ConectaIT - Área do Usuário')[0]
		self.janela.minimize()
		self.buttonIniciarJornada['text'] = 'Finalizar'
		self.eventMouseTeclado = Init_EventosMouseTeclado()
		self.NotificationPausas.start()
		self.gravareventosmouseteclado = Init_GravarEventosMouseTeclado()
		return True

class TkInit_user:
	def __init__(self, master=None):
		tstinit_notification = Thread(target=self.init_notification)
		tstinit_notification.start()
		dir_path = "C:\\ConectaIT\\modules\\user"
		user = Tk()
		user.title("ConectaIT - Área do Usuário")
		user["borderwidth"] = 0
		w = 400
		h = 270
		ws = user.winfo_screenwidth()
		hs = user.winfo_screenheight()
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		user.geometry('%dx%d+%d+%d' % (w, h, x, y))
		user.iconbitmap(dir_path+'\\..\\..\\media\\img\\icone.ico')
		user.resizable(0, 0)
		# user.overrideredirect(True)
		# user.wm_attributes("-topmost", True)
		inf = UserTemplete(user)
		user.mainloop()

	def init_notification(self):
		subprocess.call('C:\\ConectaIT\\NotificationConectaIT.exe')