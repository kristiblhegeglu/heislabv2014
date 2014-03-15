import shared
import orderlist
import time


def Init():
  shared.elev.elev_init()
  while(shared.elev.elev_get_floor_sensor_signal() != 0):
    shared.elev.elev_set_speed(-300)
  shared.elev.elev_set_speed(300)
  time.sleep(0.005)
  shared.elev.elev_set_speed(0)
  
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
  if(shared.elev.elev_get_floor_sensor_signal() != -1):
    elevator_set_speed(0)
    shared.elev.elev_set_door_open_lamp(1)
  time.sleep(1)
  shared.elev.elev_set_door_open_lamp(0)
  
  
def elevator_set_speed(speed):

  if (speed > 0):
    shared.current_dir = shared.UP
    shared.elev.elev_set_speed(300)
  
  elif (speed < 0):
    shared.current_dir = shared.DOWN
    print "jeg skal ned ikke i disko!"
    shared.elev.elev_set_speed(-300)
  
  if (speed == 0):
    if (shared.current_dir == shared.UP):
      shared.elev.elev_set_speed(-300)
      print "hei, jeg skal stoppe"
    
    elif (shared.current_dir == shared.DOWN):
      shared.elev.elev_set_speed(300)
   
    time.sleep(0.005)
    shared.elev.elev_set_speed(0)
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
    if (shared.elev_get_button_signal(shared.BUTTON_COMMAND,i)):
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
  if not (orderlist.orderlist_not_empty()):				#If orderlist is empty, set direction to NODIR and speed to 0
    elevator_set_speed(0)
    shared.target_dir = shared.NODIR
    return
    
  target_floor = -1
  
  if(direction == shared.UP):
    for i in range(shared.N_FLOORS):
      if (orderlist.orderlist_check_floor(i)):
        target_floor = i
        print "Target floor", target_floor
  
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
        print "Target floor2", target_floor

  if (target_floor == -1):
    print "This should not happen!"
    elevator_set_speed(0)
    shared.target_dir = shared.NODIR
    return
  
  if (target_floor > floor):
    elevator_set_speed(300)
    print "Target floor3", target_floor
    shared.target_dir = shared.UP
    return
    
  
  elif (target_floor < floor):
    print "Target floor3 blehd", target_floor
    elevator_set_speed(-300)
    shared.target_dir = shared.DOWN
    return
    
  elif (target_floor == floor):
    if (shared.elev.elev_get_floor_sensor_signal() == -1):
      elevator_set_speed(-300)
      print "fgsgrsgrsgreg"
      shared.target_dir = shared.NODIR
    else:
      elevator_set_speed(0)
      shared.target_dir = shared.NODIR
    return
	



#def test():
  
 # Init()
  #return False

