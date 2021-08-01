#!/usr/bin/python3

import os
import sys
import simple_http_server.server as server
from simple_http_server import request_map
from simple_http_server import Response
from simple_http_server import MultipartFile
from simple_http_server import Parameter
from simple_http_server import Parameters
from simple_http_server import Header
from simple_http_server import JSONBody
from simple_http_server import HttpError
from simple_http_server import StaticFile
from simple_http_server import Headers
from simple_http_server import Cookies
from simple_http_server import Cookie
from simple_http_server import Redirect
import logging

class Apache:
    def __init__(self):
        logging.basicConfig(filename="C:\\ConectaIT\\modules"+'\\logs\\logApache.log')
        self.iniciar_apache()

    @request_map("/")
    def mensagem():
        root = os.path.dirname(os.path.abspath(__file__))
        return StaticFile("%s/ApacheArquivos/index.html" % root, "text/html; charset=utf-8")

    @request_map("/ws.js")
    def js():
        root = os.path.dirname(os.path.abspath(__file__))
        return StaticFile("%s/ApacheArquivos/ws.js" % root)

    @request_map("/style.css")
    def style():
        root = os.path.dirname(os.path.abspath(__file__))
        return StaticFile("%s/ApacheArquivos/style.css" % root)

    def main(self, *args):
        server.start(host='127.0.0.1', port=7854)

    def iniciar_apache(self):
        logging.info("{a}".format(a=self.main()))

#Apache()