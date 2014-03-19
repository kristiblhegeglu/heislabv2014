#!/usr/bin/env python2

import orderlist
import elevator
import shared

import random
import os
import sys
import socket
import time
import json
import threading



UDP_PORT = 31715

    
def Init():
  #Creating a socket, bind, opening for broadcast
  global network_socket
  network_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  network_socket.bind(('0.0.0.0', UDP_PORT))
  network_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   
  
  return

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
  for key in shared.order_map:
    liste.append(shared.order_map[key].__dict__)
  
  msg_dict = {"type":"orderlist","orders":liste}
  network_senddata(msg_dict)
  print "Sender ordre"
  time.sleep(0.8)
  

#Function for receiving messages
def network_receiver():
  while True:
    msg, adress = network_socket.recvfrom(32000)    #receive messages, storing in msg and adress, max size 32000 bit
    if (adress[0] == shared.shared_local_ip()):
      continue
    if (len(msg) < 2):
      continue
    
    msg_dict = json.loads(msg)        #Converting from string to python object
    if msg_dict["type"] == "order":   #Checks for different types, order, elevator, lights, ping
      print "Dette skal ikke komme..."
      network_receiver_order(msg_dict)
      
    elif msg_dict["type"] == "orderlist":
      print "Test"
      network_receive_orderdict(msg_dict)
      #print order_map
      
    elif msg_dict["type"] == "ping":
      if not (adress[0] in shared.elevators):
        shared.elevators[adress[0]] = shared.Elevator(adress[0])
        print "New elevator found, with ip: ", adress[0]
      #network_receive_elevator(msg_dict,adress)
      else:
        shared.elevators[adress[0]].last_ping = time.time()
        
    else:
      print "Received data from", adress, "with payload:", msg_dict

      
def network_receiver_order(msg_dict):
  print "Received order with floor=",msg_dict["floor"],"and direction=",msg_dict["direction"]
  order = shared.Order(msg_dict["creatorID"], msg_dict["floor"], msg_dict["direction"], msg_dict["completed"], msg_dict["assigned"], msg_dict["assigned_to_id"], msg_dict["time_completed"])
  order.ID = msg_dict["ID"]
  orderlist.orderlist_get_order_map()[order.ID] = order
  
  print orderlist.orderlist_get_order_map()
  
  

def network_receive_orderdict(msg_dict):
  for order_dict in msg_dict["orders"]:
    #print order_dict
    order = shared.Order(order_dict["creatorID"],order_dict["floor"], order_dict["direction"], order_dict["completed"], order_dict["assigned"], order_dict["assigned_to_id"], order_dict["time_completed"])
    order.ID = order_dict["ID"]
    orderlist.orderlist_merge_network(order)
    print "Test2"
    

    
def network_sending():
  while(True):
    
    send_orderlist(orderlist.orderlist_get_order_map())
    
    network_send_ping(elevator.elevator_get_elevators())

  return

  
def network_send_ping(elevators):
  #liste = []
  #for key in elevators:
   # liste.append(elevators[key].__dict__)
  msg_dict = {"type":"ping"}
  network_senddata(msg_dict)
  
  time.sleep(1)



  
  
def network_connection_validator():
  while True:
    lost_ips = []
    for ip in shared.elevators:
      elevator_state = shared.elevators[ip]
      if time.time() - elevator_state.last_ping > 2.0:
        print "Lost elevator with ip:", ip
        #TODO take over orders
        lost_ips.append(ip)

    for ip in lost_ips:
      del shared.elevators[ip]
      
  time.sleep(1.0)

  
  
  

def network_threads():
  #global network_socket
  
  shared.shared_local_ip()
  
 
  
  receiver_thread = threading.Thread(target = network_receiver)
  receiver_thread.start()
  
  sending_thread = threading.Thread(target = network_sending)
  sending_thread.start()
  
  connenction_thread = threading.Thread(target = network_connection_validator)
  connenction_thread.start()
  
  
  return
  


if __name__ == "__main__":
  network_threads()

  
  
  
  
  
  
  
  

