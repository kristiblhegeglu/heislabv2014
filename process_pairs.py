#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import socket
import time
import select
import sys


UDP_PORT = 30015

count = 0

def server():
	global count
	print "Starting server"
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverSocket.setblocking(0)
	serverSocket.bind(('127.0.0.1', UDP_PORT))
	#s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	while True:
		print "Waiting for data"
		ready = select.select([serverSocket],[],[], 3)
		if ready[0]:
			data, address = serverSocket.recvfrom(1024)
			count = int(data.split()[1])		
			print "Got data:", data
		else:
			print "Other process died"
			
			break
			
	serverSocket.close()
	createDuplicate()
	client()

def client():
	global count
	print "Starting client"
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while True:
		count += 1
		data = "Count: "+str(count)
		print data
		clientSocket.sendto(data, ("127.0.0.1",UDP_PORT))
		time.sleep(2)
		
	clientSocket.close()

def createDuplicate():
	print "Spawning subproccess"
	os.popen('mate-terminal -x python2 /home/student/heislabv2014/Øving6/process_pairs.py &')
	

print len(sys.argv), sys.argv

if len(sys.argv) > 1 and sys.argv[1] == "first":
	createDuplicate()
	client()
else:
	server()
