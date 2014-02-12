#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import socket
import time

def counter():
	i = 0
	for i in range(5):
		print i+1
		time.sleep(1)


UDP_PORT = 30015

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while 1:
    data = repr(time.time()) + '\n'
    #try:
    #s.sendto(data, (counter(), UDP_PORT))
    s.sendto(data, ('Hei',UDP_PORT))
    #except:
    	#print 'Failed to send message'
    time.sleep(2)

