import shared
import orderlist
import driver

import time

    
def Init():
  #shared.elevators 
  global local_elevator
  
  local_elevator = shared.Elevator(shared.shared_local_ip(), 0, 0, shared.NODIR, shared.GetLocalElevatorId())
  shared.elevators[shared.GetLocalElevatorId()] = local_elevator
  
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
    print "UP"
    shared.current_dir = shared.UP
    shared.last_dir = shared.UP
    driver.elev.elev_set_speed(300)
  
  elif (speed < 0):
    print "DOWN"
    shared.current_dir = shared.DOWN
    shared.last_dir = shared.DOWN
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
  
  
def elevator_should_stop(floor):  
  for key in shared.order_map:
    order = shared.order_map[key]
    if (order.completed):
      continue
    if (orderlist.should_complete(order,floor)):
      return True
  
  return False
    


def elevator_get_elevators():
  return shared.elevators
 
 
def elevator_merge_network(elevator):
  if not (elevator.el_ID in shared.elevators):
    shared.elevators[elevator.el_ID] = elevator
    return  
  
 
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
    return False
    
  shared.target_floor = -1
  
  if(direction == shared.UP):
    for i in range(shared.N_FLOORS):
      if (orderlist.orderlist_check_floor(i)):
        shared.target_floor = i
  
  elif (direction == shared.DOWN):
    for i in range(shared.N_FLOORS):
      if (orderlist.orderlist_check_floor(i)):
        shared.target_floor = i
  
  if (direction == shared.NODIR) or (shared.target_floor == -1):
    for i in range(shared.N_FLOORS):
      if not (orderlist.orderlist_check_floor(i)):
        continue
      
      shared.target_floor = i


  if (shared.target_floor == -1) and (orderlist.orderlist_completed()):
    elevator_set_speed(0)
    shared.target_dir = shared.NODIR
    return False
  
  if (shared.target_floor > floor):
    elevator_set_speed(300)
    shared.target_dir = shared.UP
    return True
    
  
  elif (shared.target_floor < floor):
    elevator_set_speed(-300)
    shared.target_dir = shared.DOWN
    return True
    
  elif (shared.target_floor == floor):
    if (driver.elev.elev_get_floor_sensor_signal() == -1):
      elevator_set_speed(-300)
      shared.target_dir = shared.NODIR
      return True
    else:
      elevator_set_speed(0)
      shared.target_dir = shared.NODIR
      return False
    return False
	



#def test():
  
 # Init()
  #return False

