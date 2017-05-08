#!/usr/bin/env python

import socket
import time
import memcache


def split_multiple_messages(data):
    messages = data.split("^")
    messages = filter(None, messages)
    return messages

def parse_message(data):
    message = data.split("|")
    slabel = int(message[0])
    height = int(message[1])
    width = int(message[2])
    return {'slabel': slabel, 'height': height, 'width': width}

class SickClient:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        self.exit = False
        self.BUFFER_SIZE = 1024

    def connect(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        MESSAGE = "lets talk"
        self.s.connect((TCP_IP, TCP_PORT))
        self.s.send(MESSAGE)

    def start_comms(self):
        while not self.exit:
            data = self.s.recv(self.BUFFER_SIZE)
            print("received response: {}".format(data))
            # messages=parse_message(data)
            #format data
            #check key
            #set key
            self.mc.set("some_key", "Some value")

    def kill(self):
        self.exit = True
        self.s.close()

