package main

import (
    . "fmt" // Using '.' to avoid prefixing functions with their package names
    . "runtime" // This is probably not a good idea for large projects...
    . "time"
)

var i = 0

func adder(c chan int) {
	for x := 0; x < 1000000; x++ {
		<- c
		i++
		c <- 1
		}
	}

func subtract(c chan int) {
	for x := 0; x < 1000000; x++ {
		<- c
		i--
		c <- 1
		}
	}


func main() {
	GOMAXPROCS(NumCPU()) // I guess this is a hint to what GOMAXPROCS does...
	c := make(chan int,1)
	c <- 1	
	go adder(c) // This spawns adder() as a goroutine
	go subtract(c)
	for x := 0; x < 50; x++ {
		Println(i)
	}
    // No way to wait for the completion of a goroutine (without additional syncronization)
    // We'll come back to using channels in Exercise 2. For now: Sleep
	Sleep(1000*Millisecond)
	Println("Done:", i);
}
