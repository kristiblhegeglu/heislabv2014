import shared
import driver

import time
import threading



    
def Init():
  shared.order_map
    
  # Initialiser ordeliste
  return

# Sjekker om det finnes en ordre i en etasje, som denne heisen skal utfoere
def orderlist_check_floor(floor):
  
  if (floor < 0):
    return False
  if (orderlist_empty()):
    return False
  else: # (orderlist_empty() == 0)
    for key in shared.order_map:
      order = shared.order_map[key]
      if (order.completed):
        continue
      
      if not (order.assigned):
        continue
      
      if (order.assigned_to_id != shared.get_local_elevator_ID()):
        continue
      
      if (order.direction == shared.NODIR) and (order.creatorID != shared.get_local_elevator_ID()):
        continue
     
      
      if (order.floor == floor):
        return True
    return False

    
def orderlist_check_floor_dir(floor,direction):
  if (floor < 0):
    return False
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
        continue
      
    if not (order.assigned):
      continue
    
    if (order.assigned_to_id != shared.get_local_elevator_ID()):
      continue
    
    if (order.direction == shared.NODIR) and (order.creatorID != shared.get_local_elevator_ID()):
        continue
    
    if (order.floor == floor) and (order.direction == direction):
      return True
  return False
  
  
def orderlist_check_direction(floor, direction):
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    if (floor == order.floor) and (direction == shared.UP):
      return True
    elif (floor == order.floor) and (direction == shared.DOWN):
      return True
  return False
    
  
def should_complete(order, floor):
  if (order.floor != floor):
    return False
  
  if (order.completed):
    print "[WARNING] should_complete was called with an already completed order"
    return False
  
  if (order.direction == shared.NODIR):
    return True
  elif (order.direction == shared.last_dir):
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
  
  
def orderlist_get_distance(order, elevator_state):
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
 
def orderlist_count_assigned_orders(elevator_state):
  count = 0
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    if (order.assigned) and (order.assigned_to_id == elevator_state.el_ID):
      count += 1
  return count
    
  
def orderlist_cost_func(order, elevator_state):
  cost = 0
  
  if (order.direction == shared.NODIR):
    if (order.creatorID == elevator_state.el_ID):
      print "elevator ID er lik creatorID"
      return 0
    else:
      return shared.cost_infinity
      
      #Hvis heisen er stoppet, sett til infinity!!!
      
  if (shared.local_elevator.direction == shared.NODIR) and (elevator_state.last_floor == order.floor):
    return 0
      
  direction = orderlist_check_direction(order.floor,order.direction)
  distance = orderlist_get_distance(order, elevator_state)
      
  if (direction == shared.last_dir): #Hva skal vi bruke i stedetfor lastdir??
    cost += distance*10.0
  else:	#Moving in wrong direction
    cost += distance*30.0
      
  cost += orderlist_count_assigned_orders(elevator_state)*15
      
  if (order.assigned) and (order.assigned_to_id != elevator_state.el_ID):
    cost += 1

  return cost
  
  
def orderlist_assign_order(order):
  lowest_cost = 9999999999
  best_elevator_id = order.creatorID
  #print "Finding best candidate for order", order.ID
  for key in shared.elevators:
    elevator_state = shared.elevators[key]
    cost = orderlist_cost_func(order, elevator_state)
    #print "Cost for elevator", key, "is ", cost
    if (cost < lowest_cost):
      lowest_cost = cost
      best_elevator_id = elevator_state.el_ID
      #print "New best cost!"
  
  if not order.assigned:
    order.assigned_to_id = best_elevator_id
    order.assigned = True
    print "Assigning elevator ", best_elevator_id, " to order ", order.ID
  elif order.assigned and order.assigned_to_id != best_elevator_id:
    order.assigned_to_id = best_elevator_id
    order.assigned = True
    print "Reassigning elevator ", best_elevator_id, " to order ", order.ID
  return
  

def orderlist_reassign_elevator(elevator):
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    if not (order.assigned):
      continue
    if (order.assigned_to_id != elevator.el_ID):
      continue
    
    orderlist_assign_order(order)
  
  
def orderlist_empty():
  if (len(shared.order_map) == 0):
    return True #shared.order_map is empty, no orders
  else:
    return False #shared.order_map has orders


def orderlist_completed():
  for key,order in shared.order_map.iteritems():
    if (order.completed):
      continue
    if (order.assigned) and (order.assigned_to_id == shared.get_local_elevator_ID()):
      return False
  return True

    
def orderlist_get_order():
  for i in range(shared.N_FLOORS):
    if (driver.elev.elev_get_button_signal(shared.BUTTON_COMMAND,i)):
      orderlist_add_order(i,shared.NODIR)
      
    if (i < shared.N_FLOORS-1):
      if (driver.elev.elev_get_button_signal(shared.BUTTON_CALL_UP,i)):
        orderlist_add_order(i,shared.UP)
      
    if (i > 0):
      if (driver.elev.elev_get_button_signal(shared.BUTTON_CALL_DOWN,i)):
        orderlist_add_order(i,shared.DOWN)
  return
    
    
# Create an order from the local elevator
def orderlist_add_order(floor, direction):
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    if (order.floor == floor) and (order.direction == direction):
      return
    
  new_order = shared.Order(shared.get_local_elevator_ID(), floor, direction, False, -1, False, 0)
  orderlist_assign_order(new_order)
  
  shared.order_map[new_order.ID] = new_order
  print "New order with floor:",new_order.floor," and direction:",new_order.direction
  return

# FYY kall den mark completed
def orderlist_check_finished(floor, direction):
  for key,order in shared.order_map.iteritems():
    if (order.completed):
      continue
    if (order.floor == floor) and (should_complete(order, floor)):
      print "Order:", order.ID,"completed"
      order.completed = True
      order.time_completed = time.time()
      
    
def orderlist_clean_orders():
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

  
  
def orderlist_update_floor():
  floor = driver.elev.elev_get_floor_sensor_signal()
  if (floor == -1):
    return
  else:
    shared.local_elevator.last_floor = floor
    #print "local_elevator.last_floor: ",local_elevator.last_floor
    return shared.local_elevator.last_floor
    
  #network.SendOrderMessage(o)

def orderlist_merge_network(order):
  if not (order.ID in shared.order_map):
    if (order.completed):
      return
    shared.order_map[order.ID] = order
    print "New order from remote received:", order.ToString()
    return
  
  local_order = shared.order_map[order.ID]
  if (order.completed):
    local_order.completed = True
    
  if not local_order.assigned and order.assigned:
    print "Assigning ", order.assigned_to_id, " to order ", order.ID
    local_order.assigned_to_id = order.assigned_to_id
    local_order.assigned = True
  elif local_order.assigned and order.assigned and local_order.assigned_to_id != order.assigned_to_id:
    print "Reassigning ", order.assigned_to_id, " to order ", order.ID 
    local_order.assigned_to_id = order.assigned_to_id
    local_order.assigned = True
  
  return



def orderlist_set_lights():
  found_commands = {}
  found_up = {}
  found_down = {}
  
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    
    if (order.direction == shared.NODIR) and (order.creatorID != shared.get_local_elevator_ID()):
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
  
  
def orderlist_get_order_map():
  return shared.order_map
  


def orderlist_clean_thread():
  orderlist_thread = threading.Thread(target = orderlist_clean_orders)
  orderlist_thread.start()
  
  return

if __name__ == "__main__":
  orderlist_clean_thread
