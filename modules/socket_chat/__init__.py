#!/usr/bin/python3
import os
import sys
import json
from tkinter import *
from socket import *
from PIL import ImageTk, Image
from threading import Thread

class SocketDetalhes(object):
	def __init__(self, master=None):
		A = False