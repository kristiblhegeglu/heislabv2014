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
  
  if floor < 0:
    return False
  if (orderlist_empty()):
    return False
  else:                                 # (orderlist_empty() == 0)
    for key in shared.order_map:
      order = shared.order_map[key]
      if order.completed:
        continue
      
      if not order.assigned:
        continue
      
      if order.assigned_to_id != shared.GetLocalElevatorId():
        continue
      
      if order.direction == shared.NODIR and order.creatorID != shared.GetLocalElevatorId():
        continue
     
      
      if order.floor == floor:
        return True
    return False

    
def orderlist_check_floor_dir(floor,direction):
  if (floor < 0):
    return False
  for key in shared.order_map:
    order = shared.order_map[key]
    if order.completed:
        continue
      
    if not (order.assigned):
      continue
    
    if (order.assigned_to_id != shared.GetLocalElevatorId()):
      continue
    
    if order.direction == shared.NODIR and order.creatorID != shared.GetLocalElevatorId():
        continue
    
    if (order.floor == floor) and (order.direction == direction):
      return True 
  return False
  
  
def orderlist_check_direction(floor, direction):
  for key in shared.order_map:
    order = shared.order_map[key]
    if (floor == order.floor) and (direction == shared.UP):
      return True
    elif (floor == order.floor) and (direction == shared.DOWN):
      return True
  return False
    
  
def should_complete(order, floor):
  if (order.floor != floor):
    return False
  
  if order.completed:
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
    if (shared.current_dir == shared.UP):
      distance -= 0.5
    elif (shared.current_dir == shared.DOWN):
      distance += 0.5
    if (distance < 0):
      if (shared.current_dir == shared.UP):
        distance += 0.5
      elif (shared.current_dir == shared.DOWN):
        distance -= 0.5
  return distance
      
 
def orderlist_count_assigned_orders(elevator_state):
  count = 0
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    if (order.assigned) and (order.assigned_to_id == elevator_state.el_ID):
      count += count
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
      
  if (shared.current_dir == shared.NODIR) and (elevator_state.last_floor == order.floor):
    return 0
      
  direction = orderlist_check_direction(order.floor,order.direction)
  distance = orderlist_get_distance(order, elevator_state)
      
  if (direction == shared.last_dir): #Hva skal vi bruke i stedetfor lastdir??
    cost += distance*10.0
  else:					#Moving in wrong direction
    cost += distance*30.0
      
  cost += orderlist_count_assigned_orders(elevator_state)*15
      
  if (order.assigned) and (order.assigned_to_id != elevator_state.el_ID):
    cost += 1

  return cost
  
  
def orderlist_assign_order(order):
  lowest_cost = 0
  best_elevator_id = order.creatorID
  for key in shared.elevators:
    elevator_state = shared.elevators[key]
    cost = orderlist_cost_func(order, elevator_state)
    if (cost < lowest_cost):
      lowest_cost = cost
      best_elevator_id = elevator_state.el_ID
    
  order.assigned_to_id = best_elevator_id
  order.assigned = True
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
  if len(shared.order_map) == 0:
    return True                           #shared.order_map is empty, no orders
  else:
    return False                         #shared.order_map has orders


def orderlist_completed():
  for key,order in shared.order_map.iteritems():
    if (order.completed):
      continue
    if order.assigned and order.assigned_to_id == shared.GetLocalElevatorId():
      return False
  return True

    
def orderlist_get_order():
  for i in range(shared.N_FLOORS):
    if (driver.elev.elev_get_button_signal(shared.BUTTON_COMMAND,i)):
      orderlist_add_order(i,shared.NODIR)
      
    if(i < shared.N_FLOORS-1):
      if (driver.elev.elev_get_button_signal(shared.BUTTON_CALL_UP,i)):
        orderlist_add_order(i,shared.UP)
      
    if(i > 0):
      if (driver.elev.elev_get_button_signal(shared.BUTTON_CALL_DOWN,i)):
        orderlist_add_order(i,shared.DOWN)
  return
    
    
# Create an order from the local elevator
def orderlist_add_order(floor, direction):
  for key in shared.order_map:
    order = shared.order_map[key]
    if order.completed:
      continue
    if order.floor == floor and order.direction == direction:
      return
    
  new_order = shared.Order(shared.GetLocalElevatorId(), floor, direction, False, -1, False, 0)
  orderlist_assign_order(new_order)
  
  shared.order_map[new_order.ID] = new_order
  print "New order with floor:",new_order.floor," and direction:",new_order.direction
  return

# FYY kall den mark completed
def orderlist_check_finished(floor, direction):
  for key,order in shared.order_map.iteritems():
    if order.completed:
      continue
    if (order.floor == floor) and should_complete(order, floor):
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
    shared.last_floor = floor
    #print "last_floor: ",last_floor
    return shared.last_floor
    
  #network.SendOrderMessage(o)

def orderlist_merge_network(order):
  if not (order.ID in shared.order_map):
    if order.completed:
      return
    shared.order_map[order.ID] = order
    return
  
  local_order = shared.order_map[order.ID]
  if (order.completed):
    local_order.completed = True
  
  return



def orderlist_set_lights():
  for i in range(shared.N_FLOORS):
    if (orderlist_check_floor_dir(i,shared.NODIR)):
      driver.elev.elev_set_button_lamp(shared.BUTTON_COMMAND, i, 1)
    else:
      driver.elev.elev_set_button_lamp(shared.BUTTON_COMMAND, i, 0)
  
  for i in range(shared.N_FLOORS-1):
    if (orderlist_check_floor_dir(i,shared.UP)):
      driver.elev.elev_set_button_lamp(shared.BUTTON_CALL_UP, i, 1)
    else:
      driver.elev.elev_set_button_lamp(shared.BUTTON_CALL_UP, i, 0)
  
  for i in range(1,shared.N_FLOORS):
    if (orderlist_check_floor_dir(i,shared.DOWN)):
      driver.elev.elev_set_button_lamp(shared.BUTTON_CALL_DOWN, i, 1)
    else:
      driver.elev.elev_set_button_lamp(shared.BUTTON_CALL_DOWN, i, 0)
  
  driver.elev.elev_set_floor_indicator(shared.last_floor)
  return
  
  
def orderlist_get_order_map():
  return shared.order_map
  
#orderlist_add_order(3,shared.UP)
#for key in shared.order_map:
#  print shared.order_map[key].direction

#orderlist_get_order()

def orderlist_clean_thread():
  orderlist_thread = threading.Thread(target = orderlist_clean_orders)
  orderlist_thread.start()
  
  return

if __name__ == "__main__":
  orderlist_clean_thread

