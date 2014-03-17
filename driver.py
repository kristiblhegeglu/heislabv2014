import shared
import elevator
import orderlist

import time
import threading
import ctypes

ctypes.cdll.LoadLibrary("./elev.so")
elev = ctypes.CDLL("./elev.so")



