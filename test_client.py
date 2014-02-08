#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import socket
import sys


UDP_IP = "129.241.187.142"
UDP_PORT = 30015

 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Internet, UDP

MESSAGE = "Hello, Hege"

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

modifiedMessage, serverAddress = sock.recvfrom(2048)

print modifiedMessage



#print "UDP target IP:", UDP_IP
#print "UDP target port:", UDP_PORT
#print "message:", MESSAGE
