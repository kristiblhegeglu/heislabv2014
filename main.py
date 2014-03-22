import shared
import elevator
import orderlist
import driver
import initialization
import network

import time
import threading


#Calls to get_order, update_floor and set_lights (things that should always be done)
def Io():
  while True:
    orderlist.get_order()
    orderlist.update_floor()
    orderlist.set_lights()
    
    time.sleep(0.01)
    
  return
  
  
#Steers the elevator to choices after what state its in  
def Statemachine():
  while True:
    
    while (orderlist.orderlist_empty()):    #Waits for orders
      time.sleep(0.01)
    
    if not (elevator.controller(shared.local_elevator.last_floor, shared.target_dir)):  #If the controller isn't stopping on the last floor
      time.sleep(0.1)
      continue
    
    floor_reached = driver.elev.elev_get_floor_sensor_signal()
    if (shared.target_floor != floor_reached):    #Waits for floor reached to be equal to target_floor
      while(driver.elev.elev_get_floor_sensor_signal() != -1):
        time.sleep(0.01)
      
      while(driver.elev.elev_get_floor_sensor_signal() == -1):    #Wait in between floors
        time.sleep(0.01)
      
    floor_reached = driver.elev.elev_get_floor_sensor_signal()
    if (elevator.should_stop(floor_reached)):   #Calls to see if the elevator should stop
      elevator.set_speed(0)
      
      orderlist.mark_completed(floor_reached, shared.local_elevator.direction) #Calls to mark order as completed
      elevator.open_door()

    elif (floor_reached == 0) or (floor_reached == shared.N_FLOORS-1): #Always stop if it reaches top or bottom
      elevator.set_speed(0)
  
    time.sleep(0.01)

  return
  
  


  

def main():
  initialization.Initialization()
  
  
  
  Io_thread = threading.Thread(target = Io)     #Creates thread for IO
  Io_thread.daemon = True
  Io_thread.start()
  
  Statemachine_thread = threading.Thread(target = Statemachine)     #Creates thread for Statemachine
  Statemachine_thread.daemon = True
  Statemachine_thread.start()
  
  
  network.network_threads()  

  orderlist.clean_thread()

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
