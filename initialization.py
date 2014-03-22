import elevator
import orderlist
import shared
import network

def Initialization(): #this function initialize all the init() function in one function
  shared.Init()
  elevator.Init()
  network.Init()
  
  return
