#!/usr/bin/env python

import socket
import sys
import threading
import time
import random
import math

# NOTE: No need to import client values(this is used for testing only)
PING='ping'
CLOSE='close'

def should_send_many():
    if random.random() > 0.2:
        return True
    else:
        return False

def get_random_ship_message():
    id_part=int(math.floor(random.random()*100000))
    width=30
    height=50
    if should_send_many():
        return '^{}^'.format(CLOSE)
    return '^{}|{}|{}^'.format(id_part,width,height)

class RandomTCPThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    print("connection from: ", address)
                    while True:
                        response=get_random_ship_message()
                        if should_send_many():
                            for i in range(3):
                                client.send(response)
                                time.sleep(0.5)
                        else:
                            client.send(response)
                            time.sleep(1)
                else:
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False

class TestingTCPThreadedServer(RandomTCPThreadedServer):

    def __init__(self, host, port, messages, load):
        super(TestingTCPThreadedServer, self).__init__(host, port)
        self.messages = messages
        self.load = load

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    print("connection from: ", address)
                    while True:
                        if not self.messages:
                            client.send('^close^')
                            #TODO: exit elegantly
                            sys.exit()
                        message=self.messages.pop(0)
                        print("about to send, {}".format(message))
                        client.send(message)
                        time.sleep(1/self.load)
                else:
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False

