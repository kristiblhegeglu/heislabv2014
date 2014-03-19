import ctypes

ctypes.cdll.LoadLibrary("./elev.so")
elev = ctypes.CDLL("./elev.so")



