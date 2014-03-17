import shared
import orderlist
import driver

import time

class Elevator:
  def __init__(self, ip_address):
    self.ip = ip_address
    self.last_floor = -1  #changes later to last_floor
    self.direction = -1
    self.orders = []
    self.last_ping = time.time()

def Init():
  global elevators 
  elevators = {}
  if not(driver.elev.elev_init()):
    print "Failed to initialize"
    exit()
  
  driver.elev.elev_init()
  while(driver.elev.elev_get_floor_sensor_signal() != 0):
    driver.elev.elev_set_speed(-300)
  driver.elev.elev_set_speed(300)
  time.sleep(0.005)
  driver.elev.elev_set_speed(0)
  
  shared.current_dir = shared.NODIR
  shared.target_dir = shared.NODIR
  shared.last_floor = 0
  
  time.sleep(1)
  
  return
  
def Start():
  # Listen from driver
  # Thread for orders
  # Thread for driving elevator
  return


def elevator_open_door():
  if(driver.elev.elev_get_floor_sensor_signal() != -1):
    elevator_set_speed(0)
    driver.elev.elev_set_door_open_lamp(1)
  time.sleep(1)
  driver.elev.elev_set_door_open_lamp(0)
  
  
def elevator_set_speed(speed):

  if (speed > 0):
    shared.current_dir = shared.UP
    driver.elev.elev_set_speed(300)
  
  elif (speed < 0):
    shared.current_dir = shared.DOWN
    driver.elev.elev_set_speed(-300)
  
  if (speed == 0):
    if (shared.current_dir == shared.UP):
      driver.elev.elev_set_speed(-300)
      print "hei, jeg skal stoppe"
    
    elif (shared.current_dir == shared.DOWN):
      driver.elev.elev_set_speed(300)
   
    time.sleep(0.005)
    driver.elev.elev_set_speed(0)
    shared.current_dir = shared.NODIR
  return
  
  
def elevator_should_stop(floor,direction):
  if (orderlist.orderlist_check_floor_dir(floor,shared.NODIR)):
    return True
  if (orderlist.orderlist_check_floor_dir(floor,direction)):
    print "Stop"
    return True
  if (orderlist.orderlist_check_floor(floor)):
    return True

  return False


def elevator_check_dir(floor, direction):
  if (direction == shared.UP):
    for i in range(shared.N_FLOORS-1):
      if (orderlist.orderlist_check_floor(i)):
        return True
  elif (direction == shared.DOWN):
    for i in range(1, shared.N_FLOORS):
      if (orderlist.orderlist_check_floor(i)):
        return True
  return False
  
  
def elevator_observer():
  # Hent bestillinger, oppdater lys osv
  while True:
    # Sjekk om en knapp er trykket inn,
    if (driver.elev.elev_get_button_signal(shared.BUTTON_COMMAND,i)):
      return
    
    # Sjekk etasje sensor
    if True: # Reached new floor
      shared.LocalElevatorState.floor = floor
      #network.SendElevatorState(shared.LocalElevatorState)
      continue
    # Oppdater lys hvis man er i en etasje
    
    # Oppdater ordre lys
    orderlist.GetAllOrders()
    
    time.sleep(0.001)
  return
  

def elevator_controller(floor, direction):
  # Drive elevator to order from orderlist
  if (orderlist.orderlist_empty()):				#If orderlist is empty, set direction to NODIR and speed to 0
    elevator_set_speed(0)
    shared.target_dir = shared.NODIR
    return
    
  target_floor = -1
  
  if(direction == shared.UP):
    for i in range(shared.N_FLOORS):
      if (orderlist.orderlist_check_floor(i)):
        target_floor = i
  
  elif (direction == shared.DOWN):
    for i in range(shared.N_FLOORS):
      if (orderlist.orderlist_check_floor(i)):
        target_floor = i
  
  if (direction == shared.NODIR) or (target_floor == -1):
    min_distance = 999999
    for i in range(shared.N_FLOORS):
      if not (orderlist.orderlist_check_floor(i)):
        continue
      distance = (floor-i)*(floor-1)
      if (distance < min_distance):
        target_floor = i
        min_distance = distance

  if (target_floor == -1) and (orderlist.orderlist_completed()):
    #print "This should not happen!"
    elevator_set_speed(0)
    shared.target_dir = shared.NODIR
    return
  
  if (target_floor > floor):
    elevator_set_speed(300)
    shared.target_dir = shared.UP
    return
    
  
  elif (target_floor < floor):
    elevator_set_speed(-300)
    shared.target_dir = shared.DOWN
    return
    
  elif (target_floor == floor):
    if (driver.elev.elev_get_floor_sensor_signal() == -1):
      elevator_set_speed(-300)
      shared.target_dir = shared.NODIR
    else:
      elevator_set_speed(0)
      shared.target_dir = shared.NODIR
    return
	



#def test():
  
 # Init()
  #return False

