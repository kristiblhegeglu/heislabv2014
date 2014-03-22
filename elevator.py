import shared
import orderlist
import driver

import time


#Initializes the elevator, drives down to ground floor before taking any orders
def Init():
  
  if not (driver.elev.elev_init()): #we first check if the elevator is able to initialize itself, if not the initialization failed!
    print "Failed to initialize"
    exit()
  
  driver.elev.elev_init()
  while (driver.elev.elev_get_floor_sensor_signal() != 0):  #if not in ground floor
    driver.elev.elev_set_speed(-300)  #we set speed down
  driver.elev.elev_set_speed(300)
  time.sleep(0.005)
  driver.elev.elev_set_speed(0) #and stops when we reach ground floor
  
  shared.local_elevator.direction = shared.NODIR  #set the local elevator direction
  shared.target_dir = shared.NODIR  #set the target direction
  shared.local_elevator.last_floor = 0  #set the local elevator's last floor
  
  time.sleep(1)
  
  return

  
#Open door function
def open_door():  #this function only opens the door
  if (driver.elev.elev_get_floor_sensor_signal() != -1):  #checks if the elevator is not between floors
    set_speed(0)
    driver.elev.elev_set_door_open_lamp(1)   #set the door lamp on
  time.sleep(3) #wait 3 seconds before closing the door
  driver.elev.elev_set_door_open_lamp(0)   #turn of the door lamp
  
  
#Sets the speed of the elevator, along with changing direction for local elevator  
def set_speed(speed):
  if (speed > 0):
    print "UP"
    shared.local_elevator.direction = shared.UP #set local elevator direction
    shared.last_dir = shared.UP #set last direction
    driver.elev.elev_set_speed(300) #set speed 
  
  #the same as above
  elif (speed < 0):
    print "DOWN"
    shared.local_elevator.direction = shared.DOWN 
    shared.last_dir = shared.DOWN
    driver.elev.elev_set_speed(-300)
  
  if (speed == 0):  #if speed set to 0
    if (shared.local_elevator.direction == shared.UP):  #checks direction of the elevator
      driver.elev.elev_set_speed(-300)  
    
    elif (shared.local_elevator.direction == shared.DOWN):  #checks direction of the elevator
      driver.elev.elev_set_speed(300)
   
    time.sleep(0.005)
    driver.elev.elev_set_speed(0) #stops elevator
    shared.local_elevator.direction = shared.NODIR  #set local elevator direction
  return
  
  
#Checks if the elevator should stop in this floor accordingly to orders  
def should_stop(floor):
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed): #if the order already completed, continue
      continue
    if (orderlist.should_complete(order,floor)):  #if orderlist.should_complete(,) returns True we shall stop
      return True
  
  return False
    

#Returns the dictionary with all elevators    
def get_elevators():
  return shared.elevators
 

#If the elevator we found is not in the dictionary already, put in in with its own ID 
def merge_network(elevator):
  if not (elevator.el_ID in shared.elevators):
    shared.elevators[elevator.el_ID] = elevator
    return
  

#Controls the elevator in the right direction, accordingly to the order its supposed to take next
def controller(floor, direction):
  shared.target_floor = -1
  
  best_cost = 999999999
  best_order = None
  for key in shared.order_map:  #goes through the dictionary with all the orders
    order = shared.order_map[key]
    if (order.completed): #if order completed, continue
      continue
    if not (order.assigned) or (order.assigned_to_id != shared.get_local_elevator_ID()):  #if the order is not assigned or the local elevator id is not equal to the assigned id, continue
      continue
    
    if (order.floor == floor) and not (orderlist.should_complete(order, floor)):  #if the floor is correct but the orderlist.should_complete(,) returns False, then continue
      continue
      
    cost = orderlist.cost_func(order, shared.local_elevator)  #set cost by calling the cost function with right order and local elevator
    
    if (cost < best_cost):  #if the cost is smallers then best_cost we set both best_cost and best_order
      best_cost = cost
      best_order = order
      
  if (best_order == None):  #if best_order equals to None then retruns False
    return False
  
  shared.target_floor = best_order.floor  #set target floor to the best_order's floor

  if (shared.target_floor < 0) or (shared.target_floor >= shared.N_FLOORS): #checking for something that should not happen, target floor < 0 or target floor > 4, elevator out of reach
    print "Should not be reached"
    set_speed(0)
    shared.target_dir = shared.NODIR
    return False
  
  if (shared.target_floor > floor): #checks if we have reached target floor, if not we set the target direction in the right direction
    set_speed(300)
    shared.target_dir = shared.UP
    return True
    
  
  elif (shared.target_floor < floor): #checks if we have reached target floor, if not we set the target direction in the right direction
    set_speed(-300)
    shared.target_dir = shared.DOWN
    return True
    
  elif (shared.target_floor == floor):  #target floor equals to floor
    if (driver.elev.elev_get_floor_sensor_signal() == -1):  #if jet not reached floor drive down to floor
      set_speed(-300)
      shared.target_dir = shared.NODIR  #sets target direction to no direction
      return True
    else: #in right floor
      set_speed(0)  #shall stop
      shared.target_dir = shared.NODIR  #sets target direction to no direction
      return True
  
  print "Should never reach this"
  return False


