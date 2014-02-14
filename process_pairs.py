#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import socket
import time
import select


UDP_PORT = 30015

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(0)
s.bind(('0.0.0.0', UDP_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

i=0

while True:
	print "Waiting for data"
	ready = select.select([s],[],[], 3)
	if ready[0]:
		data, address = s.recvfrom(1024)
		i = int(data.split()[1])		
		print "Got data:", data
	else:
		print "Other process died"
		break

while True:
	i += 1
	data = "Count: "+str(i)
	print data
	s.sendto(data, ("129.241.187.255",UDP_PORT))
	time.sleep(2)

