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
	print 'Usage: ' + sys.argv[0] + ' type heuristic'
	print '\ttype: 1 = A*, 2 = RBFS'
	print '\theuristic: 1-5 are acceptable, 0 = no heuristic'

if len(sys.argv) < 3:
	printUsage()
	sys.exit(1)

arg1 = int(sys.argv[1])
arg2 = int(sys.argv[2])

# set algorithm
#alg = None
#if arg1 == 1:
#	alg = AstarSearch()
#elif arg1 == 2:
#	alg = RBFSSearch()
#else:
#	printUsage()
#	exit(2)

# set heuristic
heuristicType = arg2
if heuristicType not in [0, 1, 2, 3, 4, 5]:
	printUsage()
	exit(3)

dairy = open('./log/experiment1.txt', 'w')

for nd in range(4,11):
    print "------------------------------------------------------------"
    print "Experiment on %d disks" % nd
    direct = "./data/perms-%d.txt" % nd
    f = open(direct)
    intStates = f.readlines()
    for si in intStates:
        si = si.strip()
        if len(si) == 0:
            continue
        if si[0].isdigit():
            print "Initial State is:" + si
            if arg1 == 1:
                initialState = State()
                goalState = State()

                numDisks = len(si)
                if numDisks <= 0:
                    sys.exit("Number of disks must be greater than 0")

                for i in range(numDisks-1, -1, -1):
                    initialState.addDiskToPeg(int(si[i])+1, 0)
                    goalState.addDiskToPeg(numDisks-i, 0)
                print initialState

                alg = AstarSearch()

                problem = AstarProblem(initialState, goalState)
                startClock = clock()
                (result,numNodes) = alg.run(problem, heuristicType)
                endClock = clock()

                print "Algorithm done."
                if result == False:
                    print "Search failed!!!"
                else:
                    print "Search succeeded!"
                print "Clock: ", endClock - startClock
                print "Number of nodes explored: %d\n" % numNodes

                dairy.write("Initial State is:" + si + "\n\n")
                dairy.write("Clock: " + str(endClock - startClock) + "\n\n")
                dairy.write("Number of nodes explored: %d" % numNodes + "\n\n")

                #print result
                #for it,r in enumerate(result):
                #    print 'step %d' % it
                #    for i in range(3):
                #        print r[i]
                #print 'Total number of steps: %d' % len(result)
                #ans = raw_input("Do you want to show steps (Y/N)? ")
                #if ans.lower()[0] == 'y':
                #    print result

            if arg1 == 2:
                # set initial state
                initialState = [si, "", ""]

                # compute goal state based on input state size
                goalState = sorted(si)
                goalState.reverse()
                goalState = "".join(str(c) for c in goalState)
                goalState = [goalState,"",""]

                alg = RBFSSearch()

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
