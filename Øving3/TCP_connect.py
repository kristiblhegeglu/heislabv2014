#!/usr/bin/env python
import socket
#import sys

HOST = '129.241.187.161'    # The remote host
PORT = 33546         # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Hello, world')
data = s.recv(1024)
s.close()
print 'Received', repr(data)

