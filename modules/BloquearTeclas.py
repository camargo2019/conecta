#!/usr/bin/python3
import os
import sys
import time
import json
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
from datetime import datetime
import keyboard
from .Notifications import Notification

class BloquearTeclas:
    def __init__(self):
        #Bloquear CTRL+A
        try:
            keyboard.remove_hotkey("ctrl+a")
            keyboard.add_hotkey("ctrl+a", Notification, args=["Conecta IT", "Ops Error...", "Error[02] - Por favor, Contate o Administrador do sistema!", "client_user"])
        except:
            keyboard.remap_hotkey('ctrl+a', 'ctrl+m')
            keyboard.add_hotkey("ctrl+a", Notification, args=["Conecta IT", "Ops Error...", "Error[02] - Por favor, Contate o Administrador do sistema!", "client_user"])
        #Bloquear CTRL+C
        try:
            keyboard.remove_hotkey("ctrl+c")
            keyboard.add_hotkey("ctrl+c", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])
        except:
            keyboard.remap_hotkey('ctrl+c', 'ctrl+m')
            keyboard.add_hotkey("ctrl+c", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])
        #Bloquear CTRL+X
        try:
            keyboard.remove_hotkey("ctrl+x")
            keyboard.add_hotkey("ctrl+x", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])
        except:
            keyboard.remap_hotkey('ctrl+x', 'ctrl+m')
            keyboard.add_hotkey("ctrl+x", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])
        #Bloquear CTRL+V
        try:
            keyboard.remove_hotkey("ctrl+v")
            keyboard.add_hotkey("ctrl+v", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])
        except:
            keyboard.remap_hotkey('ctrl+v', 'ctrl+m')
            keyboard.add_hotkey("ctrl+v", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])

        #Bloquear CTRL+P
        try:
            keyboard.remove_hotkey("ctrl+p")
            keyboard.add_hotkey("ctrl+p", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])
        except:
            keyboard.remap_hotkey('ctrl+p', 'ctrl+m')
            keyboard.add_hotkey("ctrl+p", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])
        # Bloquear Print Screen
        try:
            keyboard.remove_hotkey("print screen")
            keyboard.add_hotkey("print screen", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])
        except:
            keyboard.remap_hotkey("print screen", 'ctrl+m')
            keyboard.add_hotkey("print screen", Notification, args=["Conecta IT", "Ops Error...",
                                                              "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                              "client_user"])
        #Bloquear Alt+Print Screen
        try:
            keyboard.remove_hotkey("alt+print screen")
            keyboard.add_hotkey("alt+print screen", Notification, args=["Conecta IT", "Ops Error...",
                                                                "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                "client_user"])
        except:
            keyboard.remap_hotkey("alt+print screen", 'ctrl+m')
            keyboard.add_hotkey("alt+print screen", Notification, args=["Conecta IT", "Ops Error...",
                                                                    "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                    "client_user"])
        #Bloquear Ctrl+Insert
        try:
            keyboard.remove_hotkey("ctrl+insert")
            keyboard.add_hotkey("ctrl+insert", Notification, args=["Conecta IT", "Ops Error...",
                                                                        "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                        "client_user"])
        except:
            keyboard.remap_hotkey("ctrl+insert", 'ctrl+m')
            keyboard.add_hotkey("ctrl+insert", Notification, args=["Conecta IT", "Ops Error...",
                                                                        "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                        "client_user"])
        #Bloquear Ctrl+Alt+X
        try:
            keyboard.remove_hotkey("ctrl+alt+x")
            keyboard.add_hotkey("ctrl+alt+x", Notification, args=["Conecta IT", "Ops Error...",
                                                                        "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                        "client_user"])
        except:
            keyboard.remap_hotkey("ctrl+alt+x", 'ctrl+m')
            keyboard.add_hotkey("ctrl+alt+x", Notification, args=["Conecta IT", "Ops Error...",
                                                                        "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                        "client_user"])

        #Bloquear Win+G Right|Left
        try:
            keyboard.remove_hotkey("left windows+g")
            keyboard.add_hotkey("left windows+g", Notification, args=["Conecta IT", "Ops Error...",
                                                                    "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                    "client_user"])
            keyboard.remove_hotkey("right windows+g")
            keyboard.add_hotkey("right windows+g", Notification, args=["Conecta IT", "Ops Error...",
                                                                  "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                  "client_user"])
        except:
            keyboard.remap_hotkey("left windows+g", 'ctrl+m')
            keyboard.add_hotkey("left windows+g", Notification, args=["Conecta IT", "Ops Error...",
                                                                  "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                  "client_user"])
            keyboard.remap_hotkey("right windows+g", 'ctrl+m')
            keyboard.add_hotkey("right windows+g", Notification, args=["Conecta IT", "Ops Error...",
                                                                      "Error[02] - Por favor, Contate o Administrador do sistema!",
                                                                      "client_user"])

        while True:
            time.sleep(5)