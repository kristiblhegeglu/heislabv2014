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
    elevator.elevator_controller(shared.last_floor, shared.target_dir)
    #print driver.elev.elev_get_floor_sensor_signal()
    
    while(driver.elev.elev_get_floor_sensor_signal == -1):
      time.sleep(0.001)
      
    floor_reached = driver.elev.elev_get_floor_sensor_signal()
    if(elevator.elevator_should_stop(floor_reached, shared.current_dir)):
      elevator.elevator_set_speed(0)
      
      orderlist.orderlist_check_finished(floor_reached, shared.current_dir)
      elevator.elevator_open_door()
      
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
  
  
  network.net_start()
  #network.network_sending()

  orderlist.orderlist_del_thread()
  
  #Io()
  #Statemachine()
  
  while True:
    cmd = raw_input("Type a command")
    if cmd == "list_orders":
      for key in orderlist.order_map:
        print "Order:", orderlist.order_map[key].__dict__
        
  return 
      




if __name__ == "__main__":
  main()