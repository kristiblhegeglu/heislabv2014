import ctypes

N_FLOORS = 4
BUTTON_CALL_UP = 0
BUTTON_CALL_DOWN = 1
BUTTON_COMMAND = 2
last_floor = 0

ctypes.cdll.LoadLibrary("./elev.so")
elev = ctypes.CDLL("./elev.so")


#if elev.elev_init() == 0:
  #print "Failed to initialize"
  #exit()
  
#elev.elev_set_speed(-300)


def main():
  # Initialize hardware
  if elev.elev_init() == 0:
    print "Failed to initialize"
    return 1
    exit()
  
    
  print("Press STOP button to stop elevator and exit program.\n")
  
  elev.elev_set_speed(300)
      
  while (1):
    update_floor()
    set_lights()
    if (elev.elev_get_floor_sensor_signal() == 0):
      elev.elev_set_speed(300)
      
    elif (elev.elev_get_floor_sensor_signal() == N_FLOORS-1):
      elev.elev_set_speed(-300)

    if (elev.elev_get_stop_signal()):
      elev.elev_set_speed(0)
      break

  return 0
  
def set_lights():
  i = 0
  for i in range(N_FLOORS):
    if (elev.elev_get_button_signal(BUTTON_COMMAND,i)):
      elev.elev_set_button_lamp(BUTTON_COMMAND, i, 1)
    #else:
      #elev.elev_set_button_lamp(BUTTON_COMMAND, i, 0)
      
  for i in range(N_FLOORS-1):
    if (elev.elev_get_button_signal(BUTTON_CALL_UP, i)):
      elev.elev_set_button_lamp(BUTTON_CALL_UP, i, 1)
  
  for i in range(1,N_FLOORS):
    if (elev.elev_get_button_signal(BUTTON_CALL_DOWN,i)):
      elev.elev_set_button_lamp(BUTTON_CALL_DOWN, i, 1)
  
  elev.elev_set_floor_indicator(last_floor)

def update_floor():
  global last_floor
  
  floor = elev.elev_get_floor_sensor_signal()
  if (floor == -1):
    return
  else:
    last_floor = floor

  
main()
