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
import subprocess

class BloqueioProgramas:
    def __init__(self):
        dbLocal = DataLocal()
        inf = dbLocal.dados()
        if inf["company"]["settings"]["disable_programs"] == True :
            idEmpresa = inf["company"]['id']
            db = DataBase()
            company_prog_info_db = db.programas_company(idEmpresa)
            while True:
                for program in company_prog_info_db["programs"]:
                    subprocess.call('taskkill /F /IM ' + str(program['name']))
                time.sleep(int(company_prog_info_db["time"]))
        