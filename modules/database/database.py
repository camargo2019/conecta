#!/usr/bin/python3

import os
import sys
import json
import requests
import time
from tkinter import *
from PIL import ImageTk, Image
from ..Notifications import Notification
class DataBase:
	def __init__(self):
		self.url = "http://34.95.239.34:8080"

	def login_valida(self, cpf):
		dados = json.dumps({'cpf': cpf})
		try:
			try:
				x = requests.post(self.url + "/api/activate/employee", data=dados)
			except:
				while True:
					try:
						x = requests.post(self.url+"/api/activate/employee", data=dados)
						break
					except:
						pass
					time.sleep(5)
		except:
			Notification(title="ConectaIT", subtitle="Ops..!", descrition="Error[03] - Por favor, Contate o Administrador do sistema!",
						 icone="alliance")
			return "Contate o Adminstrador do Sistema"
		dedocejson = json.loads(x.text)

		x.close()

		if (dedocejson["status"]["result"] == "error"):
			return dedocejson["status"]["message"]
		else:
			return "Sucesso"

	def dados_usuario(self, cpf):
		try:
			dados = json.dumps({'cpf': cpf})
			try:
				x = requests.post(self.url + "/api/activate/employee", data=dados)
			except:
				while True:
					try:
						x = requests.post(self.url+"/api/activate/employee", data=dados)
						break
					except:
						pass
					time.sleep(5)
		except:
			Notification(title="ConectaIT", subtitle="Ops..!", descrition="Error[03] - Por favor, Contate o Administrador do sistema!",
						 icone="alliance")
			return "Contate o Adminstrador do Sistema"
		dedocejson = json.loads(x.text)

		x.close()

		if (dedocejson["status"]["result"] == "error"):
			return False
		else:
			return dedocejson

	def ativo_user(self, id):
		try:
			try:
				x = requests.get(self.url + "/api/has/activity/"+str(id))
			except:
				while True:
					try:
						x = requests.get(self.url+"/api/has/activity/"+str(id))
						break
					except:
						pass
					time.sleep(5)
		except:
			Notification(title="ConectaIT", subtitle="Ops..!", descrition="Error[03] - Por favor, Contate o Administrador do sistema!",
						 icone="alliance")
			return "Contate o Adminstrador do Sistema"
		dedocejson = json.loads(x.text)

		x.close()

		if (dedocejson["activity"]["status"] == False):
			return False
		else:
			return True


	def ver_dados(self, cpf):
		try:
			dados = json.dumps({'cpf': cpf})
			try:
				x = requests.post(self.url + "/api/activate/employee", data=dados)
			except:
				while True:
					try:
						x = requests.post(self.url+"/api/activate/employee", data=dados)
						break
					except:
						pass
					time.sleep(5)
		except:
			Notification(title="ConectaIT", subtitle="Ops..!", descrition="Error[03] - Por favor, Contate o Administrador do sistema!",
						 icone="alliance")
			return "Contate o Adminstrador do Sistema"

		decodejson = json.loads(x.text)

		x.close()

		return decodejson

	def update_status(self, IdUser):
		try:
			dados = json.dumps({'employee_id': str(IdUser)})
			try:
				x = requests.put(self.url + "/api/register/activity", data=dados)
			except:
				while True:
					try:
						x = requests.put(self.url+"/api/register/activity", data=dados)
						break
					except:
						pass
					time.sleep(5)
		except:
			Notification(title="ConectaIT", subtitle="Ops..!", descrition="Error[03] - Por favor, Contate o Administrador do sistema!",
						 icone="alliance")
			return "Contate o Adminstrador do Sistema"

		decodejson = json.loads(x.text)

		x.close()

		return decodejson

	def update_status_end(self, IdUser):
		try:
			dados = json.dumps({'employee_id': str(IdUser)})
			try:
				x = requests.put(self.url + "/api/end/workday", data=dados)
			except:
				while True:
					try:
						x = requests.put(self.url+"/api/end/workday", data=dados)
						break
					except:
						pass
					time.sleep(5)
		except:
			Notification(title="ConectaIT", subtitle="Ops..!", descrition="Error[03] - Por favor, Contate o Administrador do sistema!",
						 icone="alliance")
			return "Contate o Adminstrador do Sistema"
		decodejson = json.loads(x.text)

		x.close()

		return decodejson


	def programas_company(self, idEmpresa):
		try:
			try:
				x = requests.get(self.url + "/api/programs/"+ str(idEmpresa))
			except:
				while True:
					try:
						x = requests.get(self.url+"/api/programs/"+ str(idEmpresa))
						break
					except:
						pass
					time.sleep(5)
		except:
			Notification(title="ConectaIT", subtitle="Ops..!", descrition="Error[03] - Por favor, Contate o Administrador do sistema!",
						 icone="alliance")
			return "Contate o Adminstrador do Sistema"
		decodejson = json.loads(x.text)

		x.close()

		return decodejson


	def init_workday_chat(self, cpf):
		dados = json.dumps({'cpf': str(cpf)})
		try:
			try:
				x = requests.post(self.url + "/api/init/workday", data=dados)
			except:
				while True:
					try:
						x = requests.post(self.url + "/api/init/workday", data=dados)
						break
					except:
						pass
					time.sleep(5)
		except:
			Notification(title="ConectaIT", subtitle="Ops..!", descrition="Error[03] - Por favor, Contate o Administrador do sistema!",
						 icone="alliance")
			return "Contate o Adminstrador do Sistema"
		decodejson = json.loads(x.text)

		x.close()

		return decodejson
