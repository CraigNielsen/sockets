#!/usr/bin/env python

import socket
import time


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
x = 'in'
while x!='out':
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    print("recieved response: {}".format(data))
    s.send("a different message")
    data = s.recv(BUFFER_SIZE)
    print("recieved response: {}".format(data))
    time.sleep(0.5)


s.close()

print("received data:", data)
