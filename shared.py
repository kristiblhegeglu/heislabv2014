import random
import socket
import time


N_FLOORS = 4

BUTTON_CALL_UP = 0
BUTTON_CALL_DOWN = 1
BUTTON_COMMAND = 2

UP = 0
DOWN = 1
NODIR = 2

target_dir = NODIR
last_dir = DOWN

target_floor = -1

cost_infinity = 999999999

order_map = {}

elevators = {}


#Creates the class Order, including all the important information about the different orders
class Order:
  def __init__(self, creatorID, floor, direction, completed,assigned, assigned_to_id, time_completed):
    self.ID = create_random_ID()
    self.creatorID = creatorID
    self.floor = floor
    self.direction = direction
    self.completed = completed
    self.assigned = assigned
    self.assigned_to_id = assigned_to_id
    self.time_completed = time_completed

  def ToString(self):
    out = "Order[floor:"+str(self.floor)+",direction="+str(self.direction)
    
    if self.completed:
      out+="COMPLETED!"
    elif self.assigned:
      out += ",assigned_to="+str(self.assigned_to_id)    
    return out
  
  def ToJson(self):
    order_dict = self.__dict__
    order_dict["type"] = "order"
    return json.dumps(order_dict)


#Creates the class Elevator, including all the important information about the states    
class Elevator:
  def __init__(self, ip_adress, last_floor, direction, last_ping, elevator_id):
    self.ip = ip_adress
    self.last_floor = last_floor 
    self.direction = direction
    self.last_ping = last_ping
    self.el_ID = elevator_id


local_elevator_ID = 0


#Initializes the local_elevators
def Init():
  global local_elevator_ID
  global local_elevator
  global elevators
  random.seed()
 
  local_elevator_ID = shared_local_ip().split('.')[3]   #The local_elevator_ID is equal to the last three numbers of the IP adress
  print "My id", local_elevator_ID
  local_elevator = Elevator(shared_local_ip(), 0, NODIR, 0, get_local_elevator_ID())
  elevators[get_local_elevator_ID()] = local_elevator
 
  
def get_local_elevator_ID():
  return local_elevator_ID
  

def create_random_ID():
  return random.randint(0, 1000000000)


#Used to find the local ip for all the elevators  
def shared_local_ip():
  global our_ip
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("gmail.com",80))
  our_ip = s.getsockname()[0]
  s.close()
  return our_ip    
        
    





