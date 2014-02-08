import socket

UDP_IP = ""
UDP_PORT = 30015

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP 
sock.bind((UDP_IP, UDP_PORT))
print "The Server is ready to receive"



while True: 
   print "Inne"
   data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
   print "Inne2"
   modifiedData = data.upper()
   sock.sendto(modifiedData, addr)
   print "received message:", data
  
print "Done"
