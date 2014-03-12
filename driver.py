import shared
import time


import ctypes

ctypes.cdll.LoadLibrary("./elev.so")
elev = ctypes.CDLL("./elev.so")

last_floor = 0




#if elev.elev_init() == 0:
  #print "Failed to initialize"
  #exit()
  
#elev.elev_set_speed(-300)

def Init():
  elev.elev_init()
  while(elev.elev_get_floor_sensor_signal() != 0):
    elev.elev_set_speed(-300)
  elev.elev_set_speed(0)
  time.sleep(3)
  return



def main():
  global elevator_current_dir
  global elevator_target_dir
  # Initialize hardware
  if elev.elev_init() == 0:
    print "Failed to initialize"
    return 1
    exit()
  
  print("Press STOP button to stop elevator and exit program.\n")
  
  Init()								#Drive down to first floor
  
  while (1):
    update_floor()
    elevator.elevator_controller(last_floor, elevator.elevator_target_dir)
    
    while(elev.elev_get_floor_sensor_signal == -1):
      time.sleep(0.001)
    floor_reached = elev.elev_get_floor_sensor_signal()
    if(elevator.elevator_should_stop(floor_reached)):
      elev.elev_set_speed(0)
    time.sleep(0.001)
  return 0
      

  #while (1):
    #update_floor()
    #set_lights()

  return 0
  
  
def test():
  if (elev.elev_get_floor_sensor_signal() == 0):
    elev.elev_set_speed(300)
      
  elif (elev.elev_get_floor_sensor_signal() == shared.N_FLOORS-1):
    elev.elev_set_speed(-300)

  if (elev.elev_get_stop_signal()):
    elev.elev_set_speed(0)
  return
  
  
  
def update_floor():
  global last_floor
  
  floor = elev.elev_get_floor_sensor_signal()
  if (floor == -1):
    return
  else:
    last_floor = floor

