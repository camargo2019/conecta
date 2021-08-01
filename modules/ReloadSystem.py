#!/usr/bin/python3
import os
import sys
import json
from socket import *
from tkinter import *
from .autoupdate import *
from .user import *
from .logged import *
import subprocess
from .database.database import *
from .database.datalocal import *
from .RequiredInternet import *

class ReloadSystem:
    def __init__(self):
        subprocess.call('C:\\ConectaIT\\ConectaIT.exe')