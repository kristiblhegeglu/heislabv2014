#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import socket
import time
import threading
import json

UDP_PORT = 31515


class Elevator:
  def __init__(self, ip_address):
    self.ip = ip_address
    self.last_floor = -1	#changes later to last_floor
    self.direction = -1
    self.orders = []
    self.last_ping = time.time()
    
elevators = {}			#Setting up a dictionary we can fill with different types


#Getting our own IP address 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
our_ip = s.getsockname()[0]
s.close()

#Creating a socket, bind, opening for broadcast 
network_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
network_socket.bind(('0.0.0.0', UDP_PORT))
network_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#Function for receiving messages
def network_receiver():
  while True:
    data_text, address = network_socket.recvfrom(1024)		#receive messages, storing in data_text and address, max size 1024 bit
    if address[0] == our_ip:
      continue
    if len(data_text) < 2:
      continue
    data = json.loads(data_text)				#Converting from string to python object
    if data["type"] == "new_order":				#Checks for different types, order, elevator, lights, ping
      print "We got a new order with floor:", data["floor"], "and button:", data["button"]
    elif data["type"] == "ping":
      if not address[0] in elevators:
	elevators[address[0]] = Elevator(address[0])
	print "New elevator found, with ip:", address[0]
      elevators[address[0]].last_ping = time.time()
    else:
      print "Received data from", address, "with payload:", data


def network_senddata(data):
  network_socket.sendto(json.dumps(data), ("129.241.187.255", UDP_PORT)) 		#Broadcasts data, converting data from python object to string
      
      
#Function for sending messages
def network_sender():
  while True:
    data = {"type":"new_order","floor":1,"button":"up"}
    network_senddata(data)
    time.sleep(2)


#Pings
def network_pinger():
  while True:
    data = {"type":"ping"}
    network_senddata(data)
    time.sleep(0.3)
    
    
#Checking if elevator is still alive and deletes ip if its dead
def network_connection_validator():
  while True:
    lost_ips = []
    for ip in elevators:
      elevator = elevators[ip]
      if time.time() - elevator.last_ping > 2.0:
	print "Lost elevator with ip:", ip
	#TODO take over orders
	lost_ips.append(ip)
	
    for ip in lost_ips:
      del elevators[ip]
  time.sleep(1.0)
  

#Starting thread for receiving messages
receiver_thread = threading.Thread(target = network_receiver)
receiver_thread.daemon = True
receiver_thread.start()


#Starting thread for sending messages
ping_thread = threading.Thread(target = network_pinger)
ping_thread.daemon = True
ping_thread.start()


#Starting connection validator thread
connection_thread = threading.Thread(target = network_connection_validator)
connection_thread.daemon = True
connection_thread.start()

network_sender()
  

      
