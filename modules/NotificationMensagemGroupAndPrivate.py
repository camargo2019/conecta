#!/usr/bin/python3
import os
import sys
import json
try:
	from .Notifications import Notification
	from win10toast import ToastNotifier
except:
	from .Notifications import Notification

from tkinter import *
from socket import *
from PIL import ImageTk, Image
from threading import Thread
from .socket_chat import *
from .logged import *
from .database.datalocal import *
from .database.database import *
#from .chat import *
class NotificationMensagemGroupAndPrivate:
	def __init__(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		client_socket = SocketDetalhes('root')
		while True:
			db = DataBase()
			msg = client_socket.recebido()
			dbLocal = DataLocal()
			infoDbLocal = dbLocal.dados()
			
			dados_client = db.dados_usuario(infoDbLocal['id'])
			cpf_client = dados_client[3]
			nome_client = dados_client[1]+" "+dados_client[9]
			nome_reponsavel = db.dados_responsavel(infoDbLocal['id'])
			try:
				msg_json = json.loads(msg)
				if(msg_json["type"] == 'group' and msg_json["cpf"] == cpf_client):
					info_user = db.login_valida(msg_json["from"])
					nomepessoa = info_user[1]
					TkInit_ChatGroup(msg_json)
					try:
						self.toaster.show_toast("ConectaIT - Chat Nova Mensagem em Grupo", nomepessoa+" Enviou uma mensagem em grupo!", icon_path=dir_path+'\\..\\..\\media\\img\\icone.ico', duration=100, threaded=True)
					except:
						Notification(title="ConectaIT", subtitle="Chat Nova Mensagem em Grupo", descrition=nomepessoa+" Enviou uma mensagem em grupo!", icone="double-bubbles")
			except:
				falss = False
#notifi = Thread(target=NotificationMensagemGroupAndPrivate)
#notifi.start()