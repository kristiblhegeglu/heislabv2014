import random

N_FLOORS = 4
BUTTON_COMMAND = 0
BUTTON_CALL_UP = 1
BUTTON_CALL_DOWN = 2

NODIR = 0
UP = 1
DOWN = 2


class ElevatorState:
  def __init__(self):
    self.floor = 0
    self.direction = BUTTON_COMMAND

LocalElevatorID = 0
LocalElevatorState = ElevatorState()

def Init():
  global LocalElevatorID
  random.seed()
  LocalElevatorID = random.randint(0, 1000000000)
  
  

def GetLocalElevatorId():
  return LocalElevatorID
  

def CreateRandomID():
  return random.randint(0, 1000000000)
