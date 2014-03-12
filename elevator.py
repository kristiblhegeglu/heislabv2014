import shared
import orderlist
import time
import driver

def Init():
  return
  
  
def Start():
  # Listen from driver
  # Thread for orders
  # Thread for driving elevator
  return


def elevator_set_speed(speed):

  if (speed > 0):
    shared.current_dir = shared.UP
    driver.elev.elev_set_speed(300)
  
  else:
    shared.current_dir = shared.DOWN
    driver.elev.elev_set_speed(-300)
  
  if (speed == 0):
    if (shared.current_dir == shared.UP):
      driver.elev.elev_set_speed(-300)
    
    else:
      driver.elev.elev_set_speed(300)
   
    time.sleep(0.05)
    driver.elev.elev_set_speed(0)
    shared.current_dir = shared.NODIR
  
  
def elevator_should_stop(floor,direction):
  if (orderlist.orderlist_check_floor_dir(floor,shared.NODIR)):
    return 1
  if (orderlist.orderlist_check_floor_dir(floor,direction)):
    return 1
  if (orderlist.orderlist_check_floor(floor)):
    return 1
  return 0
  
  
def elevator_observer():
  # Hent bestillinger, oppdater lys osv
  while True:
    # Sjekk om en knapp er trykket inn,
    if (driver.elev_get_button_signal(shared.BUTTON_COMMAND,i)):
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
  if (orderlist.orderlist_has_order() == 0):
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
  
  if (target_floor > floor):
    elevator_set_speed(300)
    shared.target_dir = shared.UP
    return
  
  elif (target_floor < floor):
    elevator_set_speed(-300)
    shared.target_dir = shared.DOWN
    return
  else:
    if (driver.elev.elev_get_floor_sensor_signal() == -1):
      elevator_set_speed(-300)
      shared.target_dir = shared.NODIR
    else:
      elevator_set_speed(0)
      shared.target_dir = shared.NODIR
    return


def test():
 
  
  driver.Init()
  
  while (1):
    orderlist.orderlist_set_lights()
    orderlist.orderlist_get_order()
    
    driver.update_floor()
    #elevator_controller(driver.last_floor, shared.target_dir)
    print 'before second while loop'  
    while(driver.elev.elev_get_floor_sensor_signal == -1):
      print 'hei, inni while loop'
      time.sleep(0.001)
    floor_reached = driver.elev.elev_get_floor_sensor_signal()
    if(elevator_should_stop(floor_reached, shared.target_dir)):
      elevator_set_speed(0)
    time.sleep(0.001)
  return 0

  
test()
