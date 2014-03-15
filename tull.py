#!/usr/bin/env python2

import random
import os
import sys
import socket
import time
import json
import threading

UDP_PORT = 31212

class Order:
  def __init__(self, creatorID, floor, direction):
    self.ID = CreateRandomID()
    self.creatorID = creatorID
    self.floor = floor
    self.direction = direction
  
  def ToString(self):
    return "Order[floor:"+str(self.floor)+",direction="+str(self.direction)+"]"
  
  def ToJson(self):
    order_dict = self.__dict__
    order_dict["type"] = "order"
    return json.dumps(order_dict)

order_map = {}
    
def CreateRandomID():
  return random.randint(0, 1000000000)

def GetLocalElevatorId():
  LocalElevatorID = random.randint(0,1000000000)
  return LocalElevatorID
    



#Function for sending messages
def network_sender(data):
  #while True:
    #data = {"type":"new_order","floor":1,"button":"up"}
  network_senddata(data)
  time.sleep(2)

def network_senddata(data):
  network_socket.sendto(json.dumps(data), ("129.241.187.255", UDP_PORT))
  
def send_orderlist(order_map):
  liste = []
  for key in order_map:
    liste.append(order_map[key].__dict__)
  
  msg_dict = {"type":"orderlist","orders":liste}
  network_senddata(msg_dict)
  

#Function for receiving messages
def network_receiver():
  while True:
    msg, address = network_socket.recvfrom(1024)    #receive messages, storing in data_text and address, max size 1024 bit
    if address[0] == our_ip:
      continue
    if len(msg) < 2:
      continue
    msg_dict = json.loads(msg)        #Converting from string to python object
    if msg_dict["type"] == "order":       #Checks for different types, order, elevator, lights, ping
      network_receiver_order(msg_dict)
    else:
      print "Received data from", address, "with payload:", msg_dict

def network_receiver_order(msg_dict):
  print "Received order with floor=",msg_dict["floor"],"and direction=",msg_dict["direction"]
  order_map = Order(msg_dict["creatorID"], msg_dict["floor"], msg_dict["direction"])
  print order_map.ToString()

    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
our_ip = s.getsockname()[0]
s.close()
    
#Creating a socket, bind, opening for broadcast 
network_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
network_socket.bind(('0.0.0.0', UDP_PORT))
network_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)    
  
new_order1 = Order(GetLocalElevatorId(),1,'UP')
new_order2 = Order(GetLocalElevatorId(),3,'UP')
new_order3 = Order(GetLocalElevatorId(),2,'DOWN')
new_order4 = Order(GetLocalElevatorId(),4,'NODIR')

order_map[new_order1.ID] = new_order1
order_map[new_order2.ID] = new_order2
order_map[new_order3.ID] = new_order3
order_map[new_order4.ID] = new_order4

for key in order_map:
  print "Got new order in floor: ",order_map[key].floor," and direction: ",order_map[key].direction
  #print "CreatorID : ",order_map[key].creatorID

print "Our IP: ",our_ip

receiver_thread = threading.Thread(target = network_receiver)
receiver_thread.daemon = True
receiver_thread.start()

while(True):
  
  send_orderlist(order_map)
  time.sleep(2)
  
  
  
  
  
  
  
  
  

