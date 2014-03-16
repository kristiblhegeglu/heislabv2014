import random


N_FLOORS = 4

BUTTON_CALL_UP = 0
BUTTON_CALL_DOWN = 1
BUTTON_COMMAND = 2

UP = 0
DOWN = 1
NODIR = 2

current_dir = NODIR
target_dir = NODIR

last_floor = 0

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
