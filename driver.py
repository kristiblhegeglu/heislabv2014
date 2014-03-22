import ctypes

ctypes.cdll.LoadLibrary("./elev.so")
elev = ctypes.CDLL("./elev.so")

#here we have "converted" all the c files from the driver we got handed out,
#so we physically didn't need to write them from c to python.
#the c files can be called by writing elev.elev_..... (the name you are looking for)

