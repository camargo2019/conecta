#!/usr/bin/python3

import os
import sys
import json
import urllib.request

class DataLocal:
    def __init__(self):
        self.dir_path = "C:\\ConectaIT\\modules\\database"
        self.arquivo = open(self.dir_path + "\\data\\database.json", "r")
        self.returndb = self.arquivo.read()

    def dados(self):
        try:
            self.decodejs = json.loads(self.returndb)
        except:
            self.decodejs = False
        return self.decodejs

    def remove_id(self):
        self.decodejs = json.loads(self.returndb)
        self.arquivo.close()
        self.decodejs["employee"]['id'] = '0'
        self.decodejs["employee"]['cpf'] = '0'
        self.stringjson = json.dumps(self.decodejs)
        #print(self.stringjson)
        self.arquivo2 = open(self.dir_path + "\\data\\database.json", "w")
        self.arquivo2.write(self.stringjson)
        self.arquivo2.close()
        return True

    def imagem_user(self):
        self.decodejs = json.loads(self.returndb)
        self.arquivo.close()
        self.url = "http://34.95.239.34:8080"
        self.img_dir = self.decodejs["employee"]['imagem']['file_path']
        self.img_name = self.decodejs["employee"]['imagem']['file_name']
        try:
            urllib.request.urlretrieve(self.url+self.img_dir+self.img_name, self.dir_path+"\\..\\logs\\img\\"+self.img_name)
        except:
            return 'nouser.png'
        return self.img_name

    def imagem_user_download_outros(self, file_path, file_name):
        self.decodejs = json.loads(self.returndb)
        self.arquivo.close()
        self.url = "http://34.95.239.34:8080"
        self.img_dir = file_path
        self.img_name = file_name
        try:
            urllib.request.urlretrieve(self.url+self.img_dir+self.img_name, self.dir_path+"\\..\\logs\\img\\"+self.img_name)
        except:
            return 'nouser.png'
        return self.img_name

    def limpar_logs(self):
        """self.arquivo = open(
            self.dir_path + '\\..\\logs\\OnKeyboardEvent.json', 'w')
        self.arquivo.close()
        self.arquivo = open(
            self.dir_path + '\\..\\logs\\OnMouseEvents.json', 'w')
        self.arquivo.close()"""
        return True

    def bloquear_teclas(self):
        self.decodejs = json.loads(self.returndb)
        self.arquivo.close()
        return self.decodejs["company"]["settings"]
