package shared

import (
  "time"
  "math"
  "fmt"
//  "log"
)

const COST_INFINITY = 9876543210

//////////////////////////
// Order system     //
//////////////////////////
type Order_t struct {
  // The unique id of the order
  ID int64
  // What floor this order was requested by or to (depending on type
  Floor int
  // The order type is DIRECTION_UP, DIRECTION_DOWN or DIRECTION_NONE
  Type int
  // The time the order was created
  TimeCreated time.Time
  // The elevator that generated this order
  CreatorUID int64
  // The elevator that currently has the responsibility to handle this order
  Assigned      bool
  AssignedToUID int64
  // The time the order was completed
  Completed     bool
  TimeCompleted time.Time
}

type ModuleOrder_t struct {
  // Channel used when an order was changed externally
  UpdatedOrderChan chan *Order_t
  UpdatedOrderRemoteChan chan *Order_t
  LostRemoteElevatorChan chan int64
  UpdatedElevatorStateChan chan *ElevatorState_t
  
  // Order map.
  OrderMap  map[int64]*Order_t
}

// Global variable for the instance of the module
var OrderModule ModuleOrder_t

/////////////////////////////////
// Order member functions
/////////////////////////////////

/**
Gets the direction to the order
**/
func (o *Order_t) GetDirectionTo(state *ElevatorState_t) int {
  //log.Print("Order = ", o, "State = ", state)
  if o.Floor == state.LastFloor {
    return DIRECTION_NONE
  } else if o.Floor > state.LastFloor {
    return DIRECTION_UP
  } else if o.Floor < state.LastFloor {
    return DIRECTION_DOWN
  }
  
  // We should never get here
  return DIRECTION_NONE
}

/**
Gets the distance to the order with a resolution of 0.5 floors.
**/
func (o *Order_t) GetDistanceTo(state *ElevatorState_t) float64 {
  var distance float64;
  distance = float64(o.Floor - state.LastFloor)
  if distance > 0 {
    if state.CurrentDirection == DIRECTION_UP {
      distance -= 0.5
    } else if state.CurrentDirection == DIRECTION_DOWN {
      distance += 0.5
    }
  } else if distance < 0 {
    if state.CurrentDirection == DIRECTION_UP {
      distance += 0.5
    } else if state.CurrentDirection == DIRECTION_DOWN {
      distance -= 0.5
    }
  }
  return math.Abs(distance)
}

/**
Count the number of orders assigned to an elevator
**/
func (o *Order_t) CountAssignedOrders(state *ElevatorState_t) int {
  count := 0
  for _, order := range(OrderModule.OrderMap) {
    if order.Completed {
      continue
    }
    if order.Assigned && order.AssignedToUID == state.UID {
      count++
    }
  }
  return count
}

/**
Calculates the cost for an elevator to take the order
**/
func (o *Order_t) Cost(state *ElevatorState_t) int {
  // Set the initial cost to zero
  cost := 0
  
  // If this is a local order and the order is a command, no other elevators can do it than the local one
  if o.Type == DIRECTION_NONE {
    if o.CreatorUID == state.UID {
      return 0
    } else {
      return COST_INFINITY
    }
  }
  
  // If the elevator is stopped
  if state.IsStopped {
    return COST_INFINITY
  }
  
  if state.CurrentDirection == DIRECTION_NONE && state.LastFloor == o.Floor {
    return 0
  }
  
  direction := o.GetDirectionTo(state)
  distance := o.GetDistanceTo(state)
  if direction == state.LastDirection {
    // We are moving in the right direction or standing still
    cost += int(distance*10.0)
  } else if state.CurrentDirection == DIRECTION_NONE && state.IsIdle {
    // The elevator is standing still and is idling
    cost += int(distance*10.0)
  } else {
    // We are moving in the wrong direction
    //log.Print("State: ", state.ToString())
    cost += int(distance*30.0)
  }
  
  // Add some cost for each order that is already assigned
  cost += o.CountAssignedOrders(state)*15
  
  // If this order is already assigned to another elevator add 1 to the cost. (Avoids equality cases)
  if o.Assigned && o.AssignedToUID != state.UID {
    cost += 1
  }
  
  return cost
}

/**
Marks an order as completed and notifies modules about the change
**/
func (o *Order_t) MarkAsCompleted() {
  o.TimeCompleted = time.Now()
  o.Completed = true
  
  // Notify the order module about the change
  OrderModule.UpdatedOrderChan <- o
  // Notify the network module about the change
  NetworkModule.UpdatedOrderChan <- o
}

/**
Create a human readable string of the order
**/
func (o *Order_t) ToString() string {
  age := int(time.Since(o.TimeCreated).Seconds())
  dir := DirectionToString(o.Type)
  return fmt.Sprintf("Order: Floor: %d, Direction: %s, Age: %d, Creator: %d, Assigned: %t, Completed: %t, Assigned To: %d", o.Floor, dir, age, o.CreatorUID, o.Assigned, o.Completed, o.AssignedToUID);
}
