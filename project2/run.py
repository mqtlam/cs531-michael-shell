#!/usr/bin/env python

from RBFSSearch import *
from Problem import *
from SearchNode import *
from time import clock, time

# Run a sample instance of RBFS Search on a problem
initialState = ["2013","",""] 
goalState = ["3210","",""]
problem = Problem(initialState, goalState)

rbfs = RBFSSearch()
startTime = time()
startClock = clock()
result = rbfs.runRBFS(problem, 1)
endClock = clock()
endTime = time()
print "\nDone with RBFS"
print "Time: ", endTime - startTime
print "Clock: ", endClock - startClock
for r in result:
	print r.state
