import shared
import elevator
import orderlist
import driver
import initialization
import network

import time
import threading



def Io():
  while(True):
    orderlist.orderlist_get_order()
    orderlist.orderlist_update_floor()
    orderlist.orderlist_set_lights()
    
    time.sleep(0.01)
    
  return
  
  
def Statemachine():
  while (True):
    
    while (orderlist.orderlist_empty()):
      time.sleep(0.001)
    
    if not elevator.elevator_controller(shared.local_elevator.last_floor, shared.target_dir):
      # We din't have anything to do, so lets wait a bit
      time.sleep(0.1)
      continue
    #print driver.elev.elev_get_floor_sensor_signal()
    
    while(driver.elev.elev_get_floor_sensor_signal() != -1):
      time.sleep(0.001)
     
    while(driver.elev.elev_get_floor_sensor_signal() == -1):
      time.sleep(0.001)
      
    floor_reached = driver.elev.elev_get_floor_sensor_signal()
    if(elevator.elevator_should_stop(floor_reached)):
      elevator.elevator_set_speed(0)
      
      orderlist.orderlist_check_finished(floor_reached, shared.local_elevator.direction)
      elevator.elevator_open_door()
    elif (floor_reached == 0) or (floor_reached == shared.N_FLOORS-1):
      elevator.elevator_set_speed(0)
      
    time.sleep(0.001)
    #print "floor reached: ",floor_reached
  return
  
  


  

def main():
  initialization.Initialization()
  
  
  
  Io_thread = threading.Thread(target = Io)
  Io_thread.daemon = True
  Io_thread.start()
  
  Statemachine_thread = threading.Thread(target = Statemachine)
  Statemachine_thread.daemon = True
  #Statemachine_thread.daemon = False
  Statemachine_thread.start()
  
  
  network.network_threads()
  #network.network_sending()

  orderlist.orderlist_clean_thread()
  
  #Io()
  #Statemachine()
  
  while True:
    cmd = raw_input("Type a command")
    if cmd == "list_orders":
      for key in shared.order_map:
        print "Order:", shared.order_map[key].__dict__
    elif cmd == "list_elevators":
      for key in shared.elevators:
        print "Elevator:", shared.elevators[key].__dict__
        
  return
      




if __name__ == "__main__":
  main()
