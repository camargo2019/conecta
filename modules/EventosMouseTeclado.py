import os
import sys
import json
import time
import pyautogui
from datetime import datetime
from threading import Thread

class EventosMouseTeclado:
    def __init__(self):
        self.dir_path = "C:\\ConectaIT\\modules"
        self.a0200evnt = Thread(target=self.OnMouseEvent)
        self.a0200evnt.start()
        """self.hm = pyHook.HookManager()
        self.hm.MouseAllButtonsDown = self.OnMouseEvent
        self.hm.KeyDown = self.OnKeyboardEvent
        self.hm.HookMouse()
        self.hm.HookKeyboard()
        pythoncom.PumpMessages()"""

    def OnMouseEvent(self):
        positionantiga = ""
        while True:
            position = pyautogui.position()
            if(positionantiga != position):
                positionantiga = position
                data = datetime.now()
                jsondump = json.dumps({'time': data.strftime('%d/%m/%Y %H:%M'), 'position': positionantiga})
                conteudo = jsondump+"\n"
                arquivo = open(self.dir_path+'\\logs\\OnMouseEvents.json', 'w')
                arquivo.writelines(conteudo)
                arquivo.close()

            time.sleep(1)
        return True

    def OnKeyboardEvent(self, event):
        data = datetime.now()
        jsondump = json.dumps({'time': data.strftime('%d/%m/%Y %H:%M'), 'messagename': event.MessageName, 'teclaID': event.KeyID,'tecla': event.Key, 'janela': event.WindowName})
        conteudo = jsondump+"\n"
        arquivo = open(self.dir_path+'\\logs\\OnKeyboardEvent.json', 'w')
        arquivo.writelines(conteudo)
        arquivo.close()
        return True
class Init_EventosMouseTeclado:
    def __init__(self):
        self.Events = Thread(target=EventosMouseTeclado)
        self.Events.start()