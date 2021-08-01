#!/usr/bin/python3
import os
import sys
import json
from socket import *
from tkinter import *
from .autoupdate import *
from .user import *
from .logged import *
from .database.database import *
from .database.datalocal import *
from .RequiredInternet import *
from media import *

class IniciaJornadaLogs:
    def __init__(self):
        arquivo = open("C:\\ConectaIT\\modules"+'\\logs\\JornadaLogs.log', 'w')
        arquivo.write('start')
        arquivo.close()

class FinalizaJornadaLogs:
    def __init__(self):
        arquivo = open("C:\\ConectaIT\\modules" + '\\logs\\JornadaLogs.log', 'w')
        arquivo.write('stop')
        arquivo.close()

class InfoJornadaLogs:
    def __init__(self):
        arquivo = open("C:\\ConectaIT\\modules" + '\\logs\\JornadaLogs.log', 'r')
        self.returnA = arquivo.read()
        arquivo.close()