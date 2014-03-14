import shared
import driver

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
    return 0
  if (orderlist_has_order() == 0):
    return 0
  else:                                 # (orderlist_has_order() == 1)
    for key in order_map:
      if order_map[key].floor == floor:
	return 1

def orderlist_check_floor_dir(floor,direction):
  global order_map
  if (floor < 0):
    return 0
  for key in order_map:
    if (orderlist_has_order() == 0):
      continue
    if (order_map[key].floor == floor) and (order_map[key].direction == direction):
      return 1 

def orderlist_has_order():
  global order_map
  if len(order_map) == 0:
    return 0                           #order_map is empty, no orders
  else:
    return 1                           #order_map has orders

    
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
    
    
# Create an order from the local elevator
def orderlist_add_order(floor, direction):
  global order_map
  new_order = Order(shared.GetLocalElevatorId(), floor, direction)
  order_map[new_order.ID] = new_order
  print "New order: ", new_order
  print "New order with floor:",new_order.floor," and direction:",new_order.direction
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
  
  driver.elev.elev_set_floor_indicator(driver.last_floor)
  
  
  
orderlist_add_order(3,shared.UP)
for key in order_map:
  print order_map[key].direction

orderlist_get_order()