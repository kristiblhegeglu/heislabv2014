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
  print "RCVBUFFER", network_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF) 
  
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
  msg_dict = {"type":"ping", "state":shared.local_elevator.__dict__}
  network_senddata(msg_dict)
  #print "sender ping", msg_dict
  

#Function for receiving messages
def network_receiver():
  last_received = time.time()
  while True:
    msg, adress = network_socket.recvfrom(32000) #receive messages, storing in msg and adress, max size 32000 bit
    if (adress[0] == shared.shared_local_ip()):
      continue
    if (len(msg) < 2):
      continue
    
    delta = time.time() - last_received
    last_received = time.time()
    if delta > 1.0:
      print "The receiver stalled, no packets for", delta, "seconds"
    
    if msg[0] != '{':
      print msg
    msg_dict = json.loads(msg) #Converting from string to python object
    
    if (msg_dict["type"] == "orderlist"):
      #print "Received orderlist", msg_dict
      network_receive_orderdict(msg_dict)
      #print order_map
    
    #elif msg_dict["type"] == "elevator_state":
    # print "Test"
    # network_receive_elevator_state(msg_dict)
      
    elif (msg_dict["type"] == "ping"):
      #print "har type ping"
      network_receive_pinger(msg_dict, adress)

    else:
      print "Received data from", adress, "with payload:", msg_dict

      

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
  el = msg_dict["state"]
  #print "mottar type ping"
  ID = el["el_ID"]
  if not (ID in shared.elevators):
    new_el = shared.Elevator(adress[0],el["last_floor"], el["direction"], time.time(), ID)
    shared.elevators[ID] = new_el
    print "New elevator found, with ip: ", adress[0]
  
  else:
    update_el_state = shared.elevators[ID]
    update_el_state.last_ping = time.time()
    update_el_state.last_floor = el["last_floor"]
    update_el_state.direction = el["direction"]
    #print "Ping"
    
   
    
def network_sending():
  last_time = time.time()
  while(True):
    delta_time = time.time() - last_time
    last_time = time.time()
    if delta_time > 1.5:
      print "Warning, sending thread has stalled!"
    
    network_send_orderlist(orderlist.orderlist_get_order_map())
    time.sleep(0.3)
    #print "#1"
    #network_send_elevator_state(elevator.elevator_get_elevators())
    
    network_send_ping(elevator.elevator_get_elevators())
    time.sleep(0.3)
    #print "#2"
    
    network_connection_validator()
    time.sleep(0.3)
    #print "#3"
  return

  

  
  
def network_connection_validator():
  #print "Sjekker connections"
  lost_ids = []
  for ID in shared.elevators:
    if (ID == shared.get_local_elevator_ID()):
      continue # can't loose the local elevator
    elevator_state = shared.elevators[ID]
    
    if ((time.time() - elevator_state.last_ping) > 4.0):
      print "Lost elevator with id:", ID, "which is ", (time.time() - elevator_state.last_ping), " seconds old"
      lost_ids.append(ID)
  for ID in lost_ids:
    del shared.elevators[ID]
    
  for ID in lost_ids:
    for key in orderlist.orderlist_get_order_map():
        order = orderlist.orderlist_get_order_map()[key]
        if order.completed:
          continue
        if not order.assigned:
          continue
        if order.direction == shared.NODIR:
          continue # Can't reassign command orders
        if (order.assigned_to_id == ID):
          orderlist.orderlist_assign_order(order)
      
    

  
  
  

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
  
  

