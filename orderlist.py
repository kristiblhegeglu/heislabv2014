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
  if floor < 0:
    return 0
  if (orderlist_has_order() == 0):
    return 0
  elif (orderlist_has_order() == 1):
    for key in order_map:
      if order_map[key] == floor:
	return 1

def orderlist_has_order():
  global order_map
  if len(order_map) == 0:
    return 0                           #order_map is empty, no orders
  else:
    return 1                           #order_map has orders

    
def ordelist_get_order():
  for i in range(shared.N_FLOORS):
    if(elev.elev_get_button_signal(shared.BUTTON_COMMAND,i)):
      orderlist_add_order(i,NODIR)
      
    elif(elev.elev_get_button_signal(shared.BUTTON_CALL_UP,i)):
      orderlist_add_order(i,UP)
      
    elif(elev.elev_get_button_signal(shared.BUTTON_CALL_DOWN,i)):
      orderlist_add_order(i,DOWN)
    
    
# Create an order from the local elevator
def orderlist_add_order(floor, direction):
  new_order = Order(shared.GetLocalElevatorId(), floor, direction)
  order_map[o.ID] = new_order
  print "New order: ", new_order
  #network.SendOrderMessage(o)

def MergeNetworkOrder(order):
  order_map[order.ID] = order
  return

# Get order local elevator should execute
def GetNextOrderToHandle():
  for key in order_map:
    return order_map[key]
  return
