import shared
import driver

import time
import threading



class Order:
  def __init__(self, creatorID, floor, direction, completed,assigned, assigned_to_id, time_completed):
    self.ID = shared.CreateRandomID()
    self.creatorID = creatorID
    self.floor = floor
    self.direction = direction
    self.completed = completed
    self.assigned = assigned
    self.assigned_to_id = assigned_to_id
    self.time_completed = time_completed
    # OSV
    
  def ToString(self):
    return "Order[floor:"+str(self.floor)+",direction="+str(self.direction)+"]"
  
  def ToJson(self):
    order_dict = self.__dict__
    order_dict["type"] = "order"
    return json.dumps(order_dict)



order_map = {}
    
def Init():
  global order_map
  # Initialiser ordeliste
  return

# Sjekker om det finnes en ordre i en etasje, som denne heisen skal utfoere
def orderlist_check_floor(floor):
  global order_map
  
  if floor < 0:
    return False
  if (orderlist_empty()):
    return False
  else:                                 # (orderlist_empty() == 0)
    for key in order_map:
      order = order_map[key]
      if order.completed:
        continue
      if order.direction == shared.NODIR and order.creatorID != shared.GetLocalElevatorId():
        continue
      if order.floor == floor:
        return True
    return False


def orderlist_check_direction(floor direction):
  global order_map
  for key in order_map:
    order = order_map[key]
    if (floor == order.floor) and (direction == shared.UP):
      return True
    elif (floor == order.floor) and (direction == shared.DOWN):
      return True
  return False
    
    
def orderlist_check_floor_dir(floor,direction):
  global order_map
  if (floor < 0):
    return False
  for key in order_map:
    order = order_map[key]
    if order.completed:
        continue
      
    #if not order.assigned:
    #  continue
    
    #if order.assigned_to_id != shared.GetLocalElevatorId():
    #  continue
    
    if order.direction == shared.NODIR and order.creatorID != shared.GetLocalElevatorId():
        continue
    
    if (order.floor == floor) and (order.direction == direction):
      return True 
  return False

  
def orderlist_get_distance():
  global order_map
  for key in order_map:
    for el in elevator.elevators:
      order = order_map[key]
      elevator_state = elevator.elevators[el]
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
      
  
def orderlist_cost_func():
  global order_map
  for key in order_map:
    for el in elevator.elevators:
      order = order_map[key]
      elevator_state = elevator.elevators
      
      if (order.direction == shared.NODIR):
	if (order.creatorID == elevator_state):
	  return False
	else:
	  return shared.cost_infinity
      
      #Hvis heisen er stoppet, sett til infinity!!!
      
      
      if (shared.current_dir == shared.NODIR) and (elevator_state.last_floor == order.floor):
	return False
      
      direction = orderlist_check_direction(floor,direction)
      distance = orderlist_get_distance()
      
      if (direction == shared.NODIR): #Hva skal vi bruke i stedetfor lastdir??
	cost += distance*10.0
      elif (shared.current_dir == shared.NODIR) and (shared.target_floor == shared.last_floor):  #and idle???
	cost += distance*10.0
      else:					#Moving in wrong direction
	cost += distance*30.0
      
      #cost += order.count_assigned_orders()*15
      
      if (order.assigned) and (order.assigned_to_id != elevator_state.el_ID):
	cost += 1

  return cost
  
def orderlist_empty():
  global order_map
  if len(order_map) == 0:
    return True                           #order_map is empty, no orders
  else:
    return False                         #order_map has orders


def orderlist_completed():
  global order_map
  for key,order in order_map.iteritems():
    if (order.completed == True):
      return True
  return False

    
def orderlist_get_order():
  global order_map
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
  global order_map
  
  if (orderlist_check_floor_dir(floor, direction)):
    return
    
  new_order = Order(shared.GetLocalElevatorId(), floor, direction, assigned, assigned_to_id, False, 0)
  order_map[new_order.ID] = new_order
  print "New order with floor:",new_order.floor," and direction:",new_order.direction
  return


def orderlist_check_finished(floor, direction):
  global order_map
  print "Should complete on floor", floor, "and dir", direction
  for key,order in order_map.iteritems():
    if order.floor == floor: # and order.direction == direction:
      print "Order completed"
      order.completed = True
      order.time_completed = time.time()
      
    
  # FYY
def orderlist_delete_order():
  global order_map
  while True:
    time.sleep(10)
    delete_list = []
    for key in order_map.keys():
      order = order_map[key]
      if (order.completed) and ((time.time() - order.time_completed) > 10.0):
        delete_list.append(key)
        
    
    for key in delete_list:
      del order_map[key]
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
  global order_map
  if not (order.ID in order_map):
    if order.completed:
      return
    order_map[order.ID] = order
    return
  
  local_order = order_map[order.ID]
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
  global order_map
  return order_map
  
#orderlist_add_order(3,shared.UP)
#for key in order_map:
#  print order_map[key].direction

#orderlist_get_order()

def orderlist_del_thread():
  orderlist_thread = threading.Thread(target = orderlist_delete_order)
  orderlist_thread.start()
  
  return

if __name__ == "__main__":
  orderlist_del_thread

