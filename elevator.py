import driver 
import shared
import orderlist
import time

elevator_current_dir = shared.NODIR
elevator_target_dir = shared.NODIR

def Init():
  driver.elev.elev_init()
  global elevator_current_dir
  global elevator_target_dir
  while(driver.elev.elev_get_floor_sensor_signal() != 0):
    elevator_set_speed(-300)
  elevator_set_speed(0)
  time.sleep(3)
  return
  
  
def Start():
  # Listen from driver
  # Thread for orders
  # Thread for driving elevator
  return


def elevator_set_speed(speed):
  global elevator_current_dir
  global elevator_target_dir
  if (speed > 0):
    elevator_current_dir = shared.UP
    driver.elev.elev_set_speed(speed)
  
  elif (speed < 0):
    elevator_current_dir = shared.DOWN
    driver.elev.elev_set_speed(speed)
  
  if (speed == 0):
    if (elevator_current_dir == shared.UP):
      driver.elev.elev_set_speed(-300)
    
    elif (elevator_current_dir == shared.DOWN):
      driver.elev.elev_set_speed(300)
   
    time.sleep(6)
    driver.elev.elev_set_speed(0)
    elevator_current_dir = shared.NODIR
  
  
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
  global elevator_current_dir
  global elevator_target_dir
  # Drive elevator to order from orderlist
  if (orderlist.orderlist_has_order() == 0):
    driver.elev.elev_set_speed(0)
    elevator_target_dir = shared.NODIR
    return
  target_floor = -1
  
  if(direction == UP):
    for i in range(shared.N_FLOORS):
      if (orderlist.orderlist_check_floor(i)):
	target_floor = i
  
  elif (direction == DOWN):
    for i in range(shared.N_FLOORS):
      if (orderlist.orderlist_check_floor(i)):
	target_floor = i
  
  if (target_floor > floor):
    driver.elev.elev_set_speed(300)
    elevator_target_dir = UP
    return
  
  elif (target_floor < floor):
    driver.elev.elev_set_speed(-300)
    elevator_target_dir = DOWN
    return
  
	
  #while True:
    # find order to complete
   # if True: # Er i etasje
      # Skal vi stoppe?
    #  continue
    #else:
      # Sett motoren i retning til ordren
     # continue
    #time.sleep(0.001)
  #return
  
  

Init()


