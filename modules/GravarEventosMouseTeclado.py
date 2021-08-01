#!/usr/bin/python3

import os
import sys
import time
import json
import requests
from tkinter import *
from PIL import ImageTk, Image
from .database.database import *
from .database.datalocal import *
from datetime import date, datetime
from threading import Thread


class GravarEventosMouseTeclado:
    def __init__(self):
        self.db = DataBase()
        self.db_base = DataLocal()
        self.dir_path = "C:\\ConectaIT\\modules"
        self.ler_dados = open(self.dir_path + "\\logs\\OnMouseEvents.json")
        self.ler_dados2 = open(self.dir_path + "\\logs\\OnKeyboardEvent.json")
        self.qntd_dados = self.ler_dados.readlines()
        self.qntd_dados2 = self.ler_dados2.readlines()
        try:
            self.file_lines = self.qntd_dados[len(self.qntd_dados) - 1]
            self.file_lines2 = self.qntd_dados2[len(self.qntd_dados2) - 1]

            self.json_decode = json.loads(self.file_lines)
            self.json_decode2 = json.loads(self.file_lines2)

            self.data_time = datetime.strptime(
                self.json_decode['time'], '%d/%m/%Y %H:%M').strftime('%d%m%Y%H%M')
            self.data_time2 = datetime.strptime(
                self.json_decode2['time'], '%d/%m/%Y %H:%M').strftime('%d%m%Y%H%M')

            self.data_time_atual = datetime.now()
            self.data_time_atual = self.data_time_atual.strftime('%d%m%Y%H%M')

            if(self.data_time and self.data_time2):
                if(self.data_time == self.data_time_atual):
                    self.dados = self.db_base.dados()
                    self.idUser = str(self.dados['employee']['id'])
                    self.inf = self.db.update_status(self.idUser)
                    #print(self.inf)
        except:
            try:
                self.file_lines = self.qntd_dados[len(self.qntd_dados) - 1]

                self.json_decode = json.loads(self.file_lines)

                self.data_time = datetime.strptime(
                    self.json_decode['time'], '%d/%m/%Y %H:%M').strftime('%d%m%Y%H%M')

                self.data_time_atual = datetime.now()
                self.data_time_atual = self.data_time_atual.strftime(
                    '%d%m%Y%H%M')

                if(self.data_time):
                    if(self.data_time == self.data_time_atual):
                        self.dados = self.db_base.dados()
                        self.idUser = str(self.dados['employee']['id'])
                        self.inf = self.db.update_status(self.idUser)
                        #print(self.inf)
            except:
                try:
                    self.file_lines2 = self.qntd_dados2[len(
                        self.qntd_dados2) - 1]
                    self.json_decode2 = json.loads(self.file_lines2)

                    self.data_time2 = datetime.strptime(
                        self.json_decode2['time'], '%d/%m/%Y %H:%M').strftime('%d%m%Y%H%M')

                    self.data_time_atual = datetime.now()
                    self.data_time_atual = self.data_time_atual.strftime(
                        '%d%m%Y%H%M')

                    if(self.data_time2):
                        if(self.data_time2 == self.data_time_atual):
                        	self.dados = self.db_base.dados()
                        	self.idUser = str(self.dados['employee']['id'])
                       		self.inf = self.db.update_status(self.idUser)
                except:
                    pass


class Init_GravarEventosMouseTeclado:
    def __init__(self):
        self.start = Thread(target=self.iniciar)
        self.start.start()

    def iniciar(self):
        while True:
            GravarEventosMouseTeclado()
            time.sleep(30)
        return True

    def stop(self):
        self.start.join(1)
        return True
