#!/usr/bin/env python
from RBFSSearch import *
from AstarSearch import *
from Problem import *
from AstarProblem import *
from SearchNode import *
from time import clock, time

import sys

## Process command line arguments

def printUsage():
	print 'Usage: ' + sys.argv[0] + ' type heuristic initialstate'
	print '\ttype: 1 = A*, 2 = RBFS'
	print '\theuristic: 1 = admissible type, 2 = non-admissible type, 0 = no heuristic'
	print '\tinitialstate: disks on peg A, top disk is leftmost, e.g. "0123"'

if len(sys.argv) < 4:
	printUsage()
	sys.exit(1)

arg1 = int(sys.argv[1])
arg2 = int(sys.argv[2])
arg3 = sys.argv[3]

# set algorithm
alg = None
if arg1 == 1:
	alg = AstarSearch()
elif arg1 == 2:
	alg = RBFSSearch()
else:
	printUsage()
	exit(2)

# set heuristic
heuristicType = arg2
if heuristicType not in [0, 1, 2, 3, 4, 5]:
	printUsage()
	exit(3)

if arg1 == 1:
    initialState = State()
    goalState = State()

    numDisks = len(arg3)
    if numDisks <= 0:
        sys.exit("Number of disks must be greater than 0")

    for i in range(numDisks-1, -1, -1):
        initialState.addDiskToPeg(int(arg3[i])+1, 0)
        goalState.addDiskToPeg(numDisks-i, 0)

    problem = AstarProblem(initialState, goalState)
    startClock = clock()
    result = alg.run(problem, heuristicType)
    endClock = clock()

    print "\nAlgorithm done."
    print "Clock: ", endClock - startClock
    #print result
    for it,r in enumerate(result):
        print 'step %d' % it
        for i in range(3):
            print r[i]
    print 'Total number of steps: %d' % len(result)
    ans = raw_input("Do you want to show steps (Y/N)? ")
    if ans.lower()[0] == 'y':
        print result

if arg1 == 2:
    # set initial state
    initialState = [arg3, "", ""]

    # compute goal state based on input state size
    goalState = sorted(arg3)
    goalState.reverse()
    goalState = "".join(str(c) for c in goalState)
    goalState = [goalState,"",""]

    ### Set up Problem
    problem = Problem(initialState, goalState)

    ### Run Problem
    startClock = time()
    result = alg.run(problem, heuristicType)
    endClock = time()

    print "\nAlgorithm done."
    print "Clock: ", endClock - startClock
    for r in result:
        print r.state
