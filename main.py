import shared
import elevator
import orderlist
import driver
import initialization
import network

import time
import threading



def Io():
  while True:
    orderlist.get_order()
    orderlist.update_floor()
    orderlist.set_lights()
    
    time.sleep(0.01)
    
  return
  
  
def Statemachine():
  while True:
    
    while (orderlist.orderlist_empty()):
      time.sleep(0.01)
    
    if not (elevator.controller(shared.local_elevator.last_floor, shared.target_dir)):
      # We din't have anything to do, so lets wait a bit
      time.sleep(0.1)
      #print "#1"
      continue
    
    floor_reached = driver.elev.elev_get_floor_sensor_signal()
    if (shared.target_floor != floor_reached): 
      # The target is not the current floor, thus we have to move
      while(driver.elev.elev_get_floor_sensor_signal() != -1):
        #print "#2"
        time.sleep(0.01)
      
      while(driver.elev.elev_get_floor_sensor_signal() == -1):
        #print "#3"
        time.sleep(0.01)
      
    floor_reached = driver.elev.elev_get_floor_sensor_signal()
    if (elevator.should_stop(floor_reached)):
      #print "#4"
      elevator.set_speed(0)
      
      orderlist.check_finished(floor_reached, shared.local_elevator.direction)
      elevator.open_door()
      #print "#6"
    elif (floor_reached == 0) or (floor_reached == shared.N_FLOORS-1):
      elevator.set_speed(0)
      #print "#7"
      
    time.sleep(0.01)
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

  orderlist.clean_thread()
  
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
    elif cmd == "my_id":
      print "My id is", shared.get_local_elevator_ID()
  return
      




if __name__ == "__main__":
  main()
