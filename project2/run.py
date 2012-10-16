#!/usr/bin/env python

from RBFSSearch import *
from Problem import *
from SearchNode import *

# Run a sample instance of RBFS Search on a problem
initialState = ([2,0,1,3], [], []) 
goalState = ([3,2,1,0], [], []) 
problem = Problem(initialState, goalState)

rbfs = RBFSSearch()
result = rbfs.runRBFS(problem, 1)
print "\nDone with RBFS"
for r in result:
	print r.state
