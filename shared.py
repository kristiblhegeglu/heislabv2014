import random
import socket
import time



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
    # OSV
    
  def ToString(self):
    return "Order[floor:"+str(self.floor)+",direction="+str(self.direction)+"]"
  
  def ToJson(self):
    order_dict = self.__dict__
    order_dict["type"] = "order"
    return json.dumps(order_dict)


class Elevator:
  def __init__(self, ip_adress, last_floor, direction, last_ping, elevator_id):
    self.ip = ip_adress
    self.last_floor = last_floor #changes later to last_floor
    self.direction = direction
    self.last_ping = last_ping
    self.el_ID = elevator_id

    
order_map = {}


elevators = {}
local_elevator = Elevator(shared_local_ip(), 0, NODIR, 0, get_local_elevator_ID())
elevators[get_local_elevator_ID()] = local_elevator


N_FLOORS = 4

BUTTON_CALL_UP = 0
BUTTON_CALL_DOWN = 1
BUTTON_COMMAND = 2

UP = 0
DOWN = 1
NODIR = 2

# SLETT bruk local_elevator.current_dir i stedet
#current_dir = NODIR
target_dir = NODIR
last_dir = DOWN

#SLETT bruk local_elevator.last_floor i stedet
#last_floor = 0

target_floor = -1

cost_infinity = 999999999

class ElevatorState:
  def __init__(self):
    self.floor = 0
    self.direction = BUTTON_COMMAND

local_elevator_ID = 0
LocalElevatorState = ElevatorState()

def Init():
  global local_elevator_ID
  random.seed()
  local_elevator_ID = random.randint(0, 1000000000)
  
  

def get_local_elevator_ID():
  return local_elevator_ID
  

def create_random_ID():
  return random.randint(0, 1000000000)

  
def shared_local_ip():
  global our_ip
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("gmail.com",80))
  our_ip = s.getsockname()[0]
  s.close()
  return our_ip
    
