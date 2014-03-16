import shared
import elevator
import orderlist
import time
import threading

import ctypes

ctypes.cdll.LoadLibrary("./elev.so")
elev = ctypes.CDLL("./elev.so")

#if elev.elev_init() == 0:
  #print "Failed to initialize"
  #exit()
  
#elev.elev_set_speed(-300)

