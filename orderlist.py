import shared
import driver



class Order:
  def __init__(self, creatorID, floor, direction, completed):
    self.ID = shared.CreateRandomID()
    self.creatorID = creatorID
    self.floor = floor
    self.direction = direction
    self.completed = False
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


def orderlist_check_floor(floor):
  global order_map
  
  if floor < 0:
    return False
  if (orderlist_empty()):
    return False
  else:                                 # (orderlist_empty() == 0)
    for key in order_map:
      if order_map[key].completed:
        continue
      if order_map[key].floor == floor:
        return True
    return False

def orderlist_check_floor_dir(floor,direction):
  global order_map
  if (floor < 0):
    return False
  for key in order_map:
    if order_map[key].completed:
        continue
    if (order_map[key].floor == floor) and (order_map[key].direction == direction):
      return True 
  return False

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
  for i in range(shared.N_FLOORS):
    if(driver.elev.elev_get_button_signal(shared.BUTTON_COMMAND,i)):
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
    
  new_order = Order(shared.GetLocalElevatorId(), floor, direction, False)
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
    
  
def orderlist_delete_order(floor, direction):
  global order_map
  for key in order_map.keys():
    if (order_map[key].floor == floor) and (order_map[key].direction == direction):
      print "slettet ordre med floor:", order_map[key].floor, "and direction:", order_map[key].direction
      del order_map[key]
      
  
  
def orderlist_update_floor():  
  floor = driver.elev.elev_get_floor_sensor_signal()
  if (floor == -1):
    return
  else:
    shared.last_floor = floor
    #print "last_floor: ",last_floor
    return shared.last_floor
    
  #network.SendOrderMessage(o)

def MergeNetworkOrder(order):
  if not order.ID in order_map:
    order_map[order.ID] = order
    return
  
  local_order = order_map[order.ID]
  if order.completed:
    local_order.completed = True
  
  return

# Get order local elevator should execute
def GetNextOrderToHandle():
  for key in order_map:
    return order_map[key]
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
  
def GetOrderMap():
  global order_map
  return order_map
  
#orderlist_add_order(3,shared.UP)
#for key in order_map:
#  print order_map[key].direction

#orderlist_get_order()