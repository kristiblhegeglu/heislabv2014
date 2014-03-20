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
  
def network_send_orderlist(order_map):
  liste = []
  for key in shared.order_map:
    liste.append(shared.order_map[key].__dict__)
  
  msg_dict = {"type":"orderlist","orders":liste}
  network_senddata(msg_dict)
  #print "Sender ordre"

  
def network_send_elevator_state(elevators):
  liste = []
  for el in shared.elevators:
    liste.append(shared.elevators[el].__dict__)
  
  msg_dict = {"type": "elevator_state", "new_elevators":liste}
  network_senddata(msg_dict)
  #print "Sender elevator_state"

  
def network_send_ping(elevators):
  liste = []
  for key in shared.elevators:
    liste.append(shared.elevators[key].__dict__)
  msg_dict = {"type":"ping", "pinger":liste}
  network_senddata(msg_dict)
  #print "sender ping", msg_dict
  
  

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
      #print "Test"
      network_receive_orderdict(msg_dict)
      #print order_map
    
    #elif msg_dict["type"] == "elevator_state":
    #  print "Test"
    #  network_receive_elevator_state(msg_dict)
      
    elif msg_dict["type"] == "ping":
      #print "har type ping"
      network_receive_pinger(msg_dict, adress)

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
    #print "Test2"
    

def network_receive_elevator_state(msg_dict):
  for el_dict in msg_dict["new_elevators"]:
    elevator_state = shared.Elevator(el_dict["ip"], orderlist.orderlist_update_floor(), el_dict["direction"], el_dict["last_ping"], el_dict["el_ID"])
    elevator.elevator_merge_network(elevator_state)
    
   
def network_receive_pinger(msg_dict, adress):
  #print "MSG_DICT", msg_dict
  for el in msg_dict["pinger"]:
    #print "mottar type ping"
    ID = el["el_ID"]
    if not (ID in shared.elevators):
      new_el = shared.Elevator(adress[0], time.time(), ID)
      shared.elevators[ID] = new_el
      print "New elevator found, with ip: ", adress[0]
      
    else:
      #Change name later!!
      elevator_state = shared.elevators[ID]
      elevator_state.last_ping = time.time()
      elevator_state.last_floor = orderlist.orderlist_update_floor()
      elevator_state.direction = el["direction"]
    
   
    
def network_sending():
  while(True):
    
    network_send_orderlist(orderlist.orderlist_get_order_map())
    
    #network_send_elevator_state(elevator.elevator_get_elevators())
    
    network_send_ping(elevator.elevator_get_elevators())
    
    network_connection_validator()
    
    time.sleep(1)

  return

  

  
  
def network_connection_validator():
  #print "Sjekker connections"
  lost_ids = []
  for ID in shared.elevators:
    if ID == shared.GetLocalElevatorId():
      continue # can't loose the local elevator
    elevator_state = shared.elevators[ID]
    
    if time.time() - elevator_state.last_ping > 4.0:
      print "Lost elevator with id:", ID
      #TODO take over orders
      lost_ids.append(ID)
  for ID in lost_ids:
    del shared.elevators[ID]
      
    

  
  
  

def network_threads():
  #global network_socket
  
  #shared.shared_local_ip()
  
 
  
  receiver_thread = threading.Thread(target = network_receiver)
  receiver_thread.start()
  
  sending_thread = threading.Thread(target = network_sending)
  sending_thread.start()
  
  ##connenction_thread = threading.Thread(target = network_connection_validator)
  ##connenction_thread.start()
  
  
  return
  


if __name__ == "__main__":
  network_threads()

  
  
  
  
  
  
  
  

