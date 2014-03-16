import shared
import elevator
import orderlist
import time
import threading
import driver
import initialization


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
    print driver.elev.elev_get_floor_sensor_signal()
    
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
  
  
Io_thread = threading.Thread(target = Io)
Io_thread.daemon = True

Statemachine_thread = threading.Thread(target = Statemachine)
Statemachine_thread.daemon = True
  

def main():
  initialization.Initialization()
    
  Io_thread.start()
  Statemachine_thread.daemon = False
  Statemachine_thread.start()
  #tull.receiver_thread.start()
  #tull.sending_thread.start()

  
  #Io()
  #Statemachine()
  
  #while True:
  #  print "All orders:" 
  #  for key in orderlist.order_map:
  #    print "Order:", orderlist.order_map[key].__dict__
  #  time.sleep(2)
  
  return 
      


main()