#!/usr/bin/python3

import os
import time
from datetime import datetime as dt
import logging
#from .database.database import *
from threading import Thread

class BloquearSites:
    def __init__(self):
        logging.basicConfig(filename="C:\\ConectaIT\\modules" + '\\logs\\logBloquearSites.log')
        #self.db = DataBase()
        self.hosts_path = "C:\Windows\System32\drivers\etc\hosts"
        self.redirect = "127.0.0.1"
        self.stop = False
        self.webSiteList = [
            "facebook.com", "www.facebook.com", "gmail.com", "www.gmail.com", "topconecta.com.br",
            "www.topconecta.com.br"
        ]
        while True:
            if dt(dt.now().year, dt.now().month, dt.now().day, 8) < dt.now() < dt(dt.now().year,
                                                                                  dt.now().month,
                                                                                  dt.now().day,
                                                                                  16):
                logging.info("Woorking Hours")
                with open(self.hosts_path, 'r+') as file:
                    self.content = file.read()
                    for website in self.webSiteList:
                        if website in self.content:
                            pass
                        else:
                            file.write(self.redirect+" "+website+"\n")
            else:
                with open(self.hosts_path, "r+") as file:
                    content = file.readlines()
                    file.seek(0)
                    for line in content:
                        if not any(website in line for website in self.webSiteList):
                            file.write(line)

                    file.truncate()

                logging.info("Fun hours...")
        time.sleep(5)

BloquearSites()
