#!/usr/bin/env python2

import random
import os
import sys
import socket
import orderlist
import time
import json
import threading
import orderlist


UDP_PORT = 31715

our_ip = 0

    



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
  global our_ip
  while True:
    msg, address = network_socket.recvfrom(1024)    #receive messages, storing in msg and address, max size 1024 bit
    if address[0] == our_ip:
      continue
    if len(msg) < 2:
      continue
    msg_dict = json.loads(msg)        #Converting from string to python object
    if msg_dict["type"] == "order":   #Checks for different types, order, elevator, lights, ping
      network_receiver_order(msg_dict)
    elif msg_dict["type"] == "orderlist":
      print "Test"
      convert_to_ordinary_dict(msg_dict)
      #print order_map
    else:
      print "Received data from", address, "with payload:", msg_dict

def network_receiver_order(msg_dict):
  print "Received order with floor=",msg_dict["floor"],"and direction=",msg_dict["direction"]
  order = orderlist.Order(msg_dict["creatorID"], msg_dict["floor"], msg_dict["direction"], msg_dict["completed"])
  order.ID = msg_dict["ID"]
  orderlist.GetOrderMap()[order.ID] = order
  
  print orderlist.GetOrderMap()
  
def convert_to_ordinary_dict(msg_dict):
  for order_dict in msg_dict["orders"]:
    #print order_dict
    order = orderlist.Order(order_dict["creatorID"],order_dict["floor"], order_dict["direction"], order_dict["completed"])
    order.ID = order_dict["ID"]
    orderlist.GetOrderMap()[order.ID] = order
    print "Test2"
    

def network_local_ip():
  global our_ip
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("gmail.com",80))
  our_ip = s.getsockname()[0]
  s.close()
    

  


def network_sending():
  while(True):
    
    send_orderlist(orderlist.GetOrderMap())
    print "Sender ordre"
    time.sleep(2)
  return
  


def net_start():
  global network_socket
  
  network_local_ip()
  
  #Creating a socket, bind, opening for broadcast 
  network_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  network_socket.bind(('0.0.0.0', UDP_PORT))
  network_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)    
  
  receiver_thread = threading.Thread(target = network_receiver)
  receiver_thread.start()
  
  sending_thread = threading.Thread(target = network_sending)
  sending_thread.start()
  return
  


if __name__ == "__main__":
  net_start()

  
  
  
  
  
  
  
  

