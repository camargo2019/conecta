#!/usr/bin/python3

import os
import sys
import json
import psutil
import subprocess
pid = os.getpid()
for proc in psutil.process_iter(['pid', 'name']):
    #jsonDecodeProc = json.loads(proc)
    #if(jsonDecodeProc['name'] == 'ConectaIT.exe'):
    inf = json.dumps(proc.info)
    inf2 = json.loads(inf)
    if(inf2['name'] == 'NotificationConectaIT.exe' and inf2['pid'] != pid):
        subprocess.call('taskkill /F /PID '+str(inf2['pid']))

from modules.NotificationIniciarJornada import *
from modules.NotificationFimJornada import *

dir_path = ""
try:
    notificationjornada = Thread(target=NotificationIniciarJornada, args=[dir_path])
    notificationjornada.start()
    notificationfimjornada = Thread(target=NotificationFimJornada, args=[dir_path])
    notificationfimjornada.start()
except:
    sys.exit()
