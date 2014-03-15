import shared



class Order:
  def __init__(self, creatorID, floor, direction):
    self.ID = shared.CreateRandomID()
    self.creatorID = creatorID
    self.floor = floor
    self.direction = direction
    # OSV
    


order_map = {}
    
def Init():
  global order_map
  # Initialiser ordeliste
  return


def orderlist_check_floor(floor):
  global order_map
  
  if floor < 0:
    return False
  if not (orderlist_not_empty()):
    return False
  else:                                 # (orderlist_not_empty() == 1)
    for key in order_map:
      if order_map[key].floor == floor:
        return True
    return False

def orderlist_check_floor_dir(floor,direction):
  global order_map
  if (floor < 0):
    return False
  for key in order_map:
    if not (orderlist_not_empty()):
      continue
    if (order_map[key].floor == floor) and (order_map[key].direction == direction):
      return True 

def orderlist_not_empty():
  global order_map
  if len(order_map) == 0:
    return False                           #order_map is empty, no orders
  else:
    return True                         #order_map has orders

    
def orderlist_get_order():
  for i in range(shared.N_FLOORS):
    if(shared.elev.elev_get_button_signal(shared.BUTTON_COMMAND,i)):
      orderlist_add_order(i,shared.NODIR)
      
    if(i < shared.N_FLOORS-1):
      if (shared.elev.elev_get_button_signal(shared.BUTTON_CALL_UP,i)):
        orderlist_add_order(i,shared.UP)
      
    if(i > 0):
      if (shared.elev.elev_get_button_signal(shared.BUTTON_CALL_DOWN,i)):
        orderlist_add_order(i,shared.DOWN)
  return
    
    
# Create an order from the local elevator
def orderlist_add_order(floor, direction):
  global order_map
  
  if (orderlist_check_floor_dir(floor, direction)):
    return
    
  new_order = Order(shared.GetLocalElevatorId(), floor, direction)
  order_map[new_order.ID] = new_order
  print "New order: ", new_order
  print "New order with floor:",new_order.floor," and direction:",new_order.direction
  return


def orderlist_check_finished(floor, direction):
  if(orderlist_check_floor_dir(floor, shared.NODIR)):
    orderlist_delete_order(floor, shared.NODIR)
  elif(orderlist_check_floor_dir(floor, shared.UP)):
    orderlist_delete_order(floor, shared.UP)
  elif(orderlist_check_floor_dir(floor, shared.DOWN)):
    orderlist_delete_order(floor, shared.DOWN)
  elif not (elevator.elevator_check_dir(floor,direction)):
    orderlist_delete_order(floor, shared.UP)
    orderlist_delete_order(floor, shared.DOWN)
  
  
def orderlist_delete_order(floor, direction):
  for key in order_map.keys():
    if (order_map[key].floor == floor) and (order_map[key].direction == direction):
      print "slettet ordre med floor:", order_map[key].floor, "and direction:", order_map[key].direction
      del order_map[key]
      
  
  
def orderlist_update_floor():  
  floor = shared.elev.elev_get_floor_sensor_signal()
  if (floor == -1):
    return
  else:
    shared.last_floor = floor
    #print "last_floor: ",last_floor
    return shared.last_floor
    
  #network.SendOrderMessage(o)

def MergeNetworkOrder(order):
  order_map[order.ID] = order
  return

# Get order local elevator should execute
def GetNextOrderToHandle():
  for key in order_map:
    return order_map[key]
  return


def orderlist_set_lights():
  for i in range(shared.N_FLOORS):
    if (orderlist_check_floor_dir(i,shared.NODIR)):
      shared.elev.elev_set_button_lamp(shared.BUTTON_COMMAND, i, 1)
    else:
      shared.elev.elev_set_button_lamp(shared.BUTTON_COMMAND, i, 0)
  
  for i in range(shared.N_FLOORS-1):
    if (orderlist_check_floor_dir(i,shared.UP)):
      shared.elev.elev_set_button_lamp(shared.BUTTON_CALL_UP, i, 1)
    else:
      shared.elev.elev_set_button_lamp(shared.BUTTON_CALL_UP, i, 0)
  
  for i in range(1,shared.N_FLOORS):
    if (orderlist_check_floor_dir(i,shared.DOWN)):
      shared.elev.elev_set_button_lamp(shared.BUTTON_CALL_DOWN, i, 1)
    else:
      shared.elev.elev_set_button_lamp(shared.BUTTON_CALL_DOWN, i, 0)
  
  shared.elev.elev_set_floor_indicator(shared.last_floor)
  return
  
  
  
#orderlist_add_order(3,shared.UP)
#for key in order_map:
#  print order_map[key].direction

#orderlist_get_order()