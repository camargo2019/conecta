#!/usr/bin/python3
import os
import sys
import json
import time
import glob
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
from datetime import datetime
from .database.datalocal import *
from .Notifications import *
import pygetwindow as gw
import subprocess

class NotificationFimJornada:
    def __init__(self, path_exec):
        self.path_exec = path_exec
        dir_path = "C:\\ConectaIT\\modules"
        for file in glob.glob(dir_path+"\\logs\\data\\*.json"):
            start = Thread(target=self.iniciar_notification, args=[file])
            start.start()

    def iniciar_notification(self, arquivo):
        dir_path = "C:\\ConectaIT\\modules"
        #print(dir_path)
        arquivo = open(arquivo, "r")
        returndb = arquivo.read()
        dados_value = json.loads(returndb)
        arquivo.close()
        while True:
            for i in dados_value['my_workday']["0"]['end']['workday_notifications']:
                try:
                    data_start = dados_value['my_workday']["0"]['end']['end_time'] + ':00'
                except:
                    data_start = "00:00:00"
                horario_atual = datetime.now().strftime('%H:%M:%S')
                iminutes, s = divmod(i["seconds"], 60)
                #print(iminutes)
                if(len(str(iminutes)) == 1):
                    time_10min = '00:0' + str(iminutes) + ':00'
                else:
                    time_10min = '00:' + str(iminutes) + ':00'
                formato = '%H:%M:%S'
                time_10 = datetime.strptime(
                    data_start, formato) - datetime.strptime(time_10min, formato)
                time_antesNotifica = datetime.strptime(
                    str(horario_atual), formato) - datetime.strptime(str(time_10), formato)
                # print(time_antesNotifica)
                # print(time_antesNotifica)
                #print(str(horario_atual)+" "+str(time))
                if(str(time_antesNotifica) == '00:00' or str(time_antesNotifica) == '00:00:00' or str(time_antesNotifica) == "0:00:00"):
                    inf = Notification(title="ConectaIT", subtitle="Atenção!",
                        descrition=i["notification"]["message"], icone="advertising", wait=i["notification"]["wait"], cancel='True')
                    if inf.returnValue == True:
                        if(i["notification"]["stay_open"] == True):
                            try:
                                janela = gw.getWindowsWithTitle('ConectaIT - Área do Usuário')[0]
                                janela.restore()
                            except:
                                subprocess.call('C:\\ConectaIT\\ConectaIT.exe')
                else:
                    time.sleep(0.5)
