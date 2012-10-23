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

# set heuristic
heuristicType = arg2
if heuristicType not in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
	printUsage()
	exit(3)

dairy = open('./log/RBFSHeur5.txt', 'w')
solen = []
numNodesExp = []
cpuHeu = []
cpuTot = []

for nd in range(4,11):
    print "------------------------------------------------------------"
    dairy.write("----------------------------------------------------------\n")
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
                #startClock = clock()
                (result,numNodes) = alg.run(problem, heuristicType)
                #endClock = clock()

                print "Algorithm done."
                if result == False:
                    print "Search failed!!!"
                    solen.append(-1)
                    dairy.write("Search failed!!!" + "\n\n")
                else:
                    print "Solution length is %d\n" % len(result)
                    solen.append(len(result))
                    dairy.write("Length of solution: %d" % len(result) + "\n\n")
                #print "Clock: ", endClock - startClock
                print "Time spend on heurisitic is %f" % alg.timeOnHeuris
                print "Time spend on Total is %f\n" % alg.timeOnTotal
                print "Number of nodes explored: %d\n" % numNodes

                numNodesExp.append(numNodes)
                cpuHeu.append(alg.timeOnHeuris)
                cpuTot.append(alg.timeOnTotal)

                dairy.write("Initial State is:" + si + "\n\n")
                dairy.write("CPU time heuristic: " + str(alg.timeOnHeuris) + "\n\n")
                dairy.write("CPU time Total: " + str(alg.timeOnTotal) + "\n\n")
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
                #startClock = time()
                result = alg.run(problem, heuristicType)
                #endClock = time()

                #print "\nAlgorithm done."
                #print "Clock: ", endClock - startClock
                #for r in result:
                #    print r.state

                print "Algorithm done."
                if result == False:
                    print "Search failed!!!"
                    solen.append(-1)
                    dairy.write("Search failed!!!" + "\n\n")
                else:
                    print "Solution length is %d\n" % len(result)
                    solen.append(len(result))
                    dairy.write("Length of solution: %d" % len(result) + "\n\n")
                #print "Clock: ", endClock - startClock
                print "Time spend on heurisitic is %f" % alg.timeOnHeuris
                print "Time spend on Total is %f\n" % alg.timeOnTotal
                print "Number of nodes explored: %d\n" % alg.numExpandedNodes

                numNodesExp.append(alg.numExpandedNodes)
                cpuHeu.append(alg.timeOnHeuris)
                cpuTot.append(alg.timeOnTotal)

                dairy.write("Initial State is:" + si + "\n\n")
                dairy.write("CPU time heuristic: " + str(alg.timeOnHeuris) + "\n\n")
                dairy.write("CPU time Total: " + str(alg.timeOnTotal) + "\n\n")
                dairy.write("Number of nodes explored: %d" % alg.numExpandedNodes + "\n\n")

#figures
#x_nodes = []
#for i in range(4,11):
#    x_nodes = x_nodes + [i]*20
#pylab.plot(range(1,len(num_clean_cells)+1), num_clean_cells)
#
#pylab.xlabel('number of actions')
#pylab.ylabel('number of clean cells')
#pylab.title('performance curve')
#pylab.grid(True)
#pylab.show()
