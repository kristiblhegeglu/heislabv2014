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


#Sends data over broadcast network with UDP and uses json.dumps to create data from a python object to a string
def senddata(data):
  network_socket.sendto(json.dumps(data), ("129.241.187.255", UDP_PORT))
  

#Preparing to send orders over network by integrating each order into a list that we put in a dictionary again  
def send_orderlist(order_map):
  liste = []
  for key in shared.order_map:    #Integrate each order into a list 
    liste.append(shared.order_map[key].__dict__)  
  
  msg_dict = {"type":"orderlist","orders":liste}  #makes the dictionary that we send broadcast
  senddata(msg_dict)


#Preparing to broadcast ping to check if the elevator is still alive 
def send_ping(elevators):
  msg_dict = {"type":"ping", "state":shared.local_elevator.__dict__}  #Dictionary we broadcast
  senddata(msg_dict)
  

#Function for receiving messages
def receiver():
  last_received = time.time()
  while True:
    msg, adress = network_socket.recvfrom(32000) #receive messages, storing in msg and adress, max size 32000 bit
    if (adress[0] == shared.shared_local_ip()): #if the adress we receive from is the same as the local ip, continue 
      continue
    if (len(msg) < 2):  #checks if the order we broadcast is valid
      continue
    
    delta = time.time() - last_received
    last_received = time.time()
    if (delta > 1.0):   #check if the packages are stalled and receive later then we want them to
      print "The receiver stalled, no packets for", delta, "seconds"
    
    if (msg[0] != '{'):
      print msg
      
    msg_dict = json.loads(msg) #Converting from string to python object
    
    if (msg_dict["type"] == "orderlist"): #if type is "orderlist" we call the function for receiving type "orderlist"
      receive_orderdict(msg_dict)

    elif (msg_dict["type"] == "ping"):  #if type is "ping" we call the function for receiving type "ping"
      receive_pinger(msg_dict, adress)

    else:
      print "Received data from", adress, "with payload:", msg_dict   #if we get a package we have not defined for our messages

      
def receive_orderdict(msg_dict):
  for order_dict in msg_dict["orders"]: #runs through the list in the dictionary
    order = shared.Order(order_dict["creatorID"],order_dict["floor"], order_dict["direction"], order_dict["completed"], order_dict["assigned"], order_dict["assigned_to_id"], order_dict["time_completed"]) #uses the class Order to create the new order
    order.ID = order_dict["ID"] #set the right id to the given order
    orderlist.merge_network(order)  #call the function that merges the local orderlist with those we broadcast
    
   
def receive_pinger(msg_dict, adress): #function for the receiving pings
  el = msg_dict["state"]
  ID = el["el_ID"]
  if not (ID in shared.elevators):  #if this ID is not already among the elevators we already have, then we got a new elevator
    new_el = shared.Elevator(adress[0],el["last_floor"], el["direction"], time.time(), ID)  #uses the class Elevator to create the new found elevator
    shared.elevators[ID] = new_el
    print "New elevator found, with ip: ", adress[0]  #shows the new elevator's ip adress
  
  else: #if not a new elevator, we update the current states for that elevator
    update_el_state = shared.elevators[ID]
    update_el_state.last_ping = time.time()
    update_el_state.last_floor = el["last_floor"]
    update_el_state.direction = el["direction"]
    
    
def sending():  #this function sends everything we want to broadcast
  last_time = time.time()
  while True:
    delta_time = time.time() - last_time
    last_time = time.time()
    if (delta_time > 1.5):  #checks if the sending is being stalled
      print "Warning, sending thread has stalled!"
    
    #broadcast the functions with 0.3 seconds between them
    send_orderlist(orderlist.get_order_map())
    time.sleep(0.3)
    
    send_ping(elevator.get_elevators())
    time.sleep(0.3)
    
    connection_validator()
    time.sleep(0.3)
    
  return
  

def connection_validator(): #checks if we lost a connection woth one of the elevators
  lost_ids = []
  for ID in shared.elevators:
    if (ID == shared.get_local_elevator_ID()):  #checks the local elevator
      continue  #can't loose the local elevator
    elevator_state = shared.elevators[ID]
    
    if ((time.time() - elevator_state.last_ping) > 4.0): #if we don't hear from a elevator for over 4.0 seconds we have lost it, by shut down or bad internet connection or no internet connection at all
      print "Lost elevator with id:", ID, "which is ", (time.time() - elevator_state.last_ping), " seconds old"
      lost_ids.append(ID) #puts all the lost elevators ips in one list
  for ID in lost_ids:
    del shared.elevators[ID]  #deletes the lost elevators
    
  for ID in lost_ids: #checks through the lost elevators if we have to reassign some of the orders the lost elevator had
    for key in orderlist.get_order_map():
        order = orderlist.get_order_map()[key]
        if (order.completed): #if the order is completed we shall ont reassign that order
          continue
        if not (order.assigned):  #the order is not given to anyone
          continue
        if (order.direction == shared.NODIR): #checks if the we have a local command, "BUTTON_COMMANDS"
          continue  #Can't reassign command orders
        if (order.assigned_to_id == ID):  #if the assigned ID and the elevator ID is the same 
          orderlist.assign_order(order) #we reassign the orders
      

def network_threads():  #creating a function that starts the threads for receiving and sending messages 
  
  receiver_thread = threading.Thread(target = receiver)
  receiver_thread.start() #starts the receiving thread
  
  sending_thread = threading.Thread(target = sending)
  sending_thread.start()  #starts the sending thread
  
  return
  


if __name__ == "__main__":
  network_threads()
  
  
  

