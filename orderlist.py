import shared
import driver

import time
import threading



#Initializes order_map
def Init():
  shared.order_map

  return

  
# Checks if there is an order on the floor, that the local elevator should execute 
def check_floor(floor):
  
  if (floor < 0):     #There is no order on a floor below 0
    return False
    
  if (orderlist_empty()):   #If there is no orders in the orderlist
    return False
    
  else:  #If there are orders in the orderlist
    for key in shared.order_map:
      order = shared.order_map[key]
      
      if (order.completed):     #If the order is completed, do nothing
        continue
      
      if not (order.assigned):  #If the order is not assigned to the specific elevator
        continue
      
      if (order.assigned_to_id != shared.get_local_elevator_ID()):  #If the order assigned to an ID is not the same as the local_elevator ID
        continue
      
      if (order.direction == shared.NODIR) and (order.creatorID != shared.get_local_elevator_ID()): #If there is a button_command and its not the local_elevator ID that took the order
        continue
      
      if (order.floor == floor):
        return True
    return False
  

#Checks if there is an order on the floor in the specific direction  
def check_floor_direction(floor, direction):
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):   #If the order is completed, do nothing
      continue
    
    if (floor == order.floor) and (direction == shared.UP):
      return True
      
    elif (floor == order.floor) and (direction == shared.DOWN):
      return True
  return False
    

#If there is an order to complete on the given floor, it should stop    
def should_complete(order, floor):
  if (order.floor != floor):
    return False
  
  if (order.completed):
    print "[WARNING] should_complete was called with an already completed order"
    return False
  
  if (order.direction == shared.NODIR):   #All the local elevators should take their own button_commands
    return True
    
  elif (order.direction == shared.last_dir):    #If there is an order on the direction the elevator last moved in
    return True
    
  if (shared.last_dir == shared.UP):
    for key in shared.order_map:
      o2 = shared.order_map[key]
      if (o2.completed):
        continue
      if (o2.floor > floor):
        return False
  
  if (shared.last_dir == shared.DOWN):
    for key in shared.order_map:
      o2 = shared.order_map[key]
      if (o2.completed):
        continue
      if (o2.floor < floor):
        return False
  
  return True
  

#Calculates the distance all the elevators has between the floor the order is on, and the one they were last one  
def get_distance(order, elevator_state):
  distance = order.floor - elevator_state.last_floor
  if (distance > 0):
    if (shared.local_elevator.direction == shared.UP):
      distance -= 0.5
      
    elif (shared.local_elevator.direction == shared.DOWN):
      distance += 0.5
      
    if (distance < 0):
      if (shared.local_elevator.direction == shared.UP):
        distance += 0.5
        
      elif (shared.local_elevator.direction == shared.DOWN):
        distance -= 0.5
        
  return abs(distance)      
 

#Counts the number of assigned orders for all the elevators 
def count_assigned_orders(elevator_state):      
  count = 0
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    
    if (order.assigned) and (order.assigned_to_id == elevator_state.el_ID):
      count += 1
      
  return count
    

#The cost function, deciding which elevator is best suited for which order    
def cost_func(order, elevator_state):
  cost = 0
  
  if (order.direction == shared.NODIR):       
    if (order.creatorID == elevator_state.el_ID):   #The local elevator should always take button_commands
      print "elevator ID er lik creatorID"
      return 0
      
    else:
      return shared.cost_infinity
      
  if (shared.local_elevator.direction == shared.NODIR) and (elevator_state.last_floor == order.floor):    #If the local elevator already is on the floor
    return 0
      
  direction = check_floor_direction(order.floor,order.direction)
  distance = get_distance(order, elevator_state)
      
  if (direction == shared.last_dir):  #If the ordered direction is the same as the elevator moves in
    cost += distance*10.0
    
  else:     #Moving in wrong direction
    cost += distance*30.0
      
  cost += count_assigned_orders(elevator_state)*15      #A higher cost if the elevator is already assigned
      
  if (order.assigned) and (order.assigned_to_id != elevator_state.el_ID):   #If the order is already assigned, and not to the local elevator
    cost += 1

  return cost
  

#Assigns orders to the elevators accordingly to cost  
def assign_order(order):
  lowest_cost = 9999999999
  best_elevator_id = order.creatorID
  for key in shared.elevators:
    elevator_state = shared.elevators[key]
    cost = cost_func(order, elevator_state)

    if (cost < lowest_cost):      #If cost for this elevator is better than for the last, change
      lowest_cost = cost
      best_elevator_id = elevator_state.el_ID
  
  if not (order.assigned):        #if the order hasn't been assigned, change it to True
    order.assigned_to_id = best_elevator_id
    order.assigned = True
    print "Assigning elevator ", best_elevator_id, " to order ", order.ID
    
  elif (order.assigned) and (order.assigned_to_id != best_elevator_id):   #If it has been assigned, but it's different from the best elevator
    order.assigned_to_id = best_elevator_id
    order.assigned = True
    print "Reassigning elevator ", best_elevator_id, " to order ", order.ID
    
  return


#Checks if there are any orders in the orderlist  
def orderlist_empty():
  if (len(shared.order_map) == 0):
    return True #shared.order_map is empty, no orders
    
  else:
    return False #shared.order_map has orders


#Checks if there is a button pushed, sending this to add order    
def get_order():
  for i in range(shared.N_FLOORS):
    if (driver.elev.elev_get_button_signal(shared.BUTTON_COMMAND,i)):
      add_order(i,shared.NODIR)
      
    if (i < shared.N_FLOORS-1):
      if (driver.elev.elev_get_button_signal(shared.BUTTON_CALL_UP,i)):
        add_order(i,shared.UP)
      
    if (i > 0):
      if (driver.elev.elev_get_button_signal(shared.BUTTON_CALL_DOWN,i)):
        add_order(i,shared.DOWN)
        
  return
    
    
# Adds order to the orderlist
def add_order(floor, direction):
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    
    if (order.floor == floor) and (order.direction == direction): #If the order is already in the list
      return
    
  new_order = shared.Order(shared.get_local_elevator_ID(), floor, direction, False, -1, False, 0)
  assign_order(new_order)     #Calls assign to find the best elevator
  
  shared.order_map[new_order.ID] = new_order
  print "New order with floor:",new_order.floor," and direction:",new_order.direction
  return


#Marks the order as completed if an elevator has executed it  
def mark_completed(floor, direction):
  for key,order in shared.order_map.iteritems():
    if (order.completed):
      continue
    
    if (order.floor == floor) and (should_complete(order, floor)):
      print "Order:", order.ID,"completed"
      order.completed = True
      order.time_completed = time.time()
      

#Cleans the orderlist of completed orders that has been there for more than ten seconds      
def clean_orders():
  while True:
    time.sleep(10)
    delete_list = []
    for key in shared.order_map.keys():
      order = shared.order_map[key]
      if (order.completed) and ((time.time() - order.time_completed) > 10.0):
        delete_list.append(key)
    
    for key in delete_list:
      del shared.order_map[key]
      print "sletter ordre: ", key


#Updates the last floor the local elevator passed      
def update_floor():
  floor = driver.elev.elev_get_floor_sensor_signal()
  if (floor == -1):
    return
    
  else:
    shared.local_elevator.last_floor = floor
    return shared.local_elevator.last_floor


#Merges with the network for the orders    
def merge_network(order):
  if not (order.ID in shared.order_map):  #If the order is not already in the map, it's received from another elevator
    if (order.completed):
      return
      
    shared.order_map[order.ID] = order
    print "New order from remote received:", order.ToString()
    return
  
  local_order = shared.order_map[order.ID]
  if (order.completed):
    local_order.completed = True
    
  if not (local_order.assigned) and (order.assigned):   #If order not local assigned, or assigned
    print "Assigning ", order.assigned_to_id, " to order ", order.ID
    local_order.assigned_to_id = order.assigned_to_id
    local_order.assigned = True
    
  elif (local_order.assigned) and (order.assigned) and (local_order.assigned_to_id != order.assigned_to_id): #If the order is assigned, but the local order ID is unequal to the one the order is assigned to already 
    print "Reassigning ", order.assigned_to_id, " to order ", order.ID    #Reassigning orders to another elevator
    local_order.assigned_to_id = order.assigned_to_id
    local_order.assigned = True
  
  return


#Sets the lights on the buttons that have been pushed
def set_lights():
  found_commands = {}
  found_up = {}
  found_down = {}
  
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    
    if (order.direction == shared.NODIR) and (order.creatorID != shared.get_local_elevator_ID()):   #Should not set_lights if there is button_commands on another elevator
      continue
    
    if (order.direction == shared.NODIR):
      found_commands[order.floor] = True
      
    elif (order.direction == shared.UP) and (order.floor < shared.N_FLOORS-1):
      found_up[order.floor] = True
      
    elif (order.direction == shared.DOWN) and (order.floor > 0):
      found_down[order.floor] = True    
   
  for floor in range(shared.N_FLOORS):
    if (floor in found_commands):
      driver.elev.elev_set_button_lamp(shared.BUTTON_COMMAND, floor, 1)
    else:
      driver.elev.elev_set_button_lamp(shared.BUTTON_COMMAND, floor, 0)
  
  for floor in range(shared.N_FLOORS-1):
    if (floor in found_up):
      driver.elev.elev_set_button_lamp(shared.BUTTON_CALL_UP, floor, 1)
    else:
      driver.elev.elev_set_button_lamp(shared.BUTTON_CALL_UP, floor, 0)
      
  for floor in range(1, shared.N_FLOORS):
    if (floor in found_down):
      driver.elev.elev_set_button_lamp(shared.BUTTON_CALL_DOWN, floor, 1)
    else:
      driver.elev.elev_set_button_lamp(shared.BUTTON_CALL_DOWN, floor, 0)
  
  driver.elev.elev_set_floor_indicator(shared.local_elevator.last_floor)
  return
  

#Returns the updated orderlist  
def get_order_map():
  return shared.order_map
  

#Starts the thread for cleaning orders
def clean_thread():
  orderlist_thread = threading.Thread(target = clean_orders)
  orderlist_thread.start()
  
  return

  
if __name__ == "__main__":
  clean_thread
