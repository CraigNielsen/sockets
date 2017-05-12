#!/usr/bin/env python

import socket
import time
import memcache

CLOSE='close'
PING='ping'

def split_multiple_messages(data):
    messages = data.split("^")
    messages = filter(None, messages)
    return messages


def message_is_close(message):
    return message==CLOSE

def message_is_ping(message):
    return message==PING

def parse_message(single_message):
    message = single_message.split("|")
    if len(message) == 1:
        if message_is_ping(message[0]):
            return PING
        if message_is_close(message[0]):
            return CLOSE
        # TODO: logging instead. do not break.. handle this
        raise Exception('unknown message received: {}'.format(single_message))
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

    def checks(self):
        self.mc.set("memcache_up", "true")
        assert self.mc.get("memcache_up")=="true" ,"memcache is down"

    def connect(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        MESSAGE = "lets talk"
        self.s.connect((TCP_IP, TCP_PORT))
        self.s.send(MESSAGE)
        self.checks()

    def set_memcache_key(self, message):
        if not self.mc.get(message['slabel']):
            self.mc.set(message['slabel'], 'processed')
            return True
        else:
            return False

    def act_on_message_types(self, message):
        '''
            logic to decide what to do on different message types
        '''
        if message_is_ping(message):
            print("got your ping")
        elif message_is_close(message):
            self.kill()
        elif self.set_memcache_key(message):
            do_something(message)
        else:
            print("doubled slabel message {}".format(message['slabel']))

    def start_comms(self):
        while not self.exit:
            data = self.s.recv(self.BUFFER_SIZE)
            if data:
                time.sleep(0.2)
                print("received comms: {}".format(data))

                messages = split_multiple_messages(data)
                al = map(parse_message, messages)
                map(self.act_on_message_types, al)
                # split_multiple_messages
                # parse_message
            else:
                self.kill()
            # messages=parse_message(data)
            #format data
            #check key
            #set key

    def kill(self):
        self.exit = True
        self.s.close()

