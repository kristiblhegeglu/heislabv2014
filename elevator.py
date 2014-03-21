import shared
import orderlist
import driver

import time


#Initializes the elevator, drives down to ground floor before taking any orders
def Init():
  #shared.elevators
  
  if not (driver.elev.elev_init()):
    print "Failed to initialize"
    exit()
  
  driver.elev.elev_init()
  while (driver.elev.elev_get_floor_sensor_signal() != 0):
    driver.elev.elev_set_speed(-300)
  driver.elev.elev_set_speed(300)
  time.sleep(0.005)
  driver.elev.elev_set_speed(0)
  
  shared.local_elevator.direction = shared.NODIR
  shared.target_dir = shared.NODIR
  shared.local_elevator.last_floor = 0
  
  time.sleep(1)
  
  return
  
  
def Start():
  # Listen from driver
  # Thread for orders
  # Thread for driving elevator
  return

  
#Open door function
def open_door():
  if (driver.elev.elev_get_floor_sensor_signal() != -1):
    set_speed(0)
    driver.elev.elev_set_door_open_lamp(1)
  time.sleep(1)
  driver.elev.elev_set_door_open_lamp(0)
  
  
#Sets the speed of the elevator, along with changing direction for local elevator  
def set_speed(speed):
  if (speed > 0):
    print "UP"
    shared.local_elevator.direction = shared.UP
    shared.last_dir = shared.UP
    driver.elev.elev_set_speed(300)
  
  elif (speed < 0):
    print "DOWN"
    shared.local_elevator.direction = shared.DOWN
    shared.last_dir = shared.DOWN
    driver.elev.elev_set_speed(-300)
  
  if (speed == 0):
    if (shared.local_elevator.direction == shared.UP):
      driver.elev.elev_set_speed(-300)
      print "hei, jeg skal stoppe"
    
    elif (shared.local_elevator.direction == shared.DOWN):
      driver.elev.elev_set_speed(300)
   
    time.sleep(0.005)
    driver.elev.elev_set_speed(0)
    shared.local_elevator.direction = shared.NODIR
  return
  
  
#Checks if the elevator should stop in this floor accordingly to orders  
def should_stop(floor):
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    if (orderlist.should_complete(order,floor)):
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
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    if not (order.assigned) or (order.assigned_to_id != shared.get_local_elevator_ID()):
      continue
    
    if (order.floor == floor) and not (orderlist.should_complete(order, floor)):
      continue
      
    cost = orderlist.cost_func(order, shared.local_elevator)
    
    if (cost < best_cost):
      best_cost = cost
      best_order = order
      
  if (best_order == None):
    #print "#1337"
    return False
  
  shared.target_floor = best_order.floor
  #print "#1338", best_order.__dict__

  if (shared.target_floor < 0) or (shared.target_floor >= shared.N_FLOORS):
    print "Should not be reached"
    set_speed(0)
    shared.target_dir = shared.NODIR
    return False
  
  if (shared.target_floor > floor):
    set_speed(300)
    shared.target_dir = shared.UP
    return True
    
  
  elif (shared.target_floor < floor):
    set_speed(-300)
    shared.target_dir = shared.DOWN
    return True
    
  elif (shared.target_floor == floor):
    if (driver.elev.elev_get_floor_sensor_signal() == -1):
      set_speed(-300)
      shared.target_dir = shared.NODIR
      return True
    else:
      set_speed(0)
      shared.target_dir = shared.NODIR
      return True
  
  print "Should never reach this"
  return False

