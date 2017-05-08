#!/usr/bin/env python

import socket
import time
import memcache


def split_multiple_messages(data):
    messages = data.split("^")
    messages = filter(None, messages)
    return messages

def determine_message_is_ping(message):
    return message=="ping"

def parse_message(data):
    message = data.split("|")
    slabel = message[0]
    height = int(message[1])
    width = int(message[2])
    return {'slabel': slabel, 'height': height, 'width': width}

def do_something(message):
    print("sending message through {}".format(message))

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

    def update_wms(self, message):
        #will get decorator for cache key checking
        if not self.mc.get(message['slabel']):
            self.mc.set(message['slabel'], 'processed')
            do_something(message)

    def start_comms(self):
        while not self.exit:
            data = self.s.recv(self.BUFFER_SIZE)
            if data:
                print("received comms: {}".format(data))
                import pdb
                pdb.set_trace()

                messages = split_multiple_messages(data)
                final = map(self.update_wms, map(parse_message, messages))
                print(final)
                # split_multiple_messages
                # parse_message
                # update_wms()
            else:
                self.kill()
            # messages=parse_message(data)
            #format data
            #check key
            #set key

    def kill(self):
        self.exit = True
        self.s.close()

