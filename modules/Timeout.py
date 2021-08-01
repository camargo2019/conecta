#!/usr/bin/python3
from threading import Thread
from time import sleep
from .RequiredInternet import RequiredInternet

class IntervalRunner:
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.executing = False

    def run(self):
        self.executing = True
        while self.executing:
            RequiredInternet()
            sleep(self.interval)

    def stop(self):
        self.executing = False