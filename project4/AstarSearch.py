#!/usr/bin/env python
#from AstarProblem import *
#from Heuristic import *
#import heapq
from util import PriorityQueueWithFunction
from time import *
#import copy

NMAX = 1000000 # make this value small to control time
# actions are: f, tl + f, tr + f, tl + tl + f
neigh = [
        [(0,1),(-1,0),(1,0),(0,-1)], # 0 = u
        [(1,0),(0,1),(0,-1),(-1,0)], # 1 = r
        [(0,-1),(1,0),(-1,0),(0,1)], # 2 = d
        [(-1,0),(0,-1),(0,1),(1,0)], # 3 = l
        ]

class AstarProblem:
    def __init__(self, initialState, goalState, allowed):
        "initState is [(x,y),dir], goalState is (x,y)"
        self.initialState = initialState
        self.goalState = goalState
        self.map = allowed
        print '-------------------------------------'
        print 'allowed:'
        print allowed
        print '-------------------------------------'
        print 'goals:'
        print goalState
        print '-------------------------------------'
        print 'current:'
        print initialState

    def isAllowed(self,square):
        try:
            ind = self.map.index(square)
        except ValueError:
            ind = -1
        if ind == -1:
            return False
        else:
            return True

    def heuristic(self,current):
        "without considering direction"
        "minimum block dist(current, goalState[i])"
        (x,y) = current[0]
        minDist = -1
        for g in self.goalState:
            (xg,yg) = g
            #print (xg,yg)
            dist = abs(xg-x) + abs(yg-y)
            if  dist < minDist:
                minDist = dist
        return minDist

    def goalTest(self, state):
        #return state[0] == self.goalState[0]
        for gs in self.goalState:
            if state[0] == gs:
                return True
        return False

    def nextStates(self, curState):
        (x,y) = curState[0]
        d = curState[1]
        states = [(x,y+1),(x+1,y),(x,y-1),(x-1,y)] # u-0 r-1 d-2 l-3
        retStates = []
        for i,s in enumerate(states):
            if self.isAllowed(s) == True:
                retStates = retStates + [[s,i]]
        #print '* nextStates:'
        #print retStates
        return (retStates)

class AstarSearch:
    def __init__(self,problem):
        self.numExpandedNodes = 0
        self.problem = problem
        self.frontier = PriorityQueueWithFunction(self.fcost)
        self.timeOnHeuris = 0
        self.timeOnTotal = 0

    def run(self):
        "estimate running time of A*"

        if self.problem.goalState == []:
            print '*** No goals, no actions'
            print '\n'
            return []

        t1 = time()
        (result,nNodes) = self.Astar()
        t2 = time()
        self.timeOnTotal = t2 - t1
        #print "Explored %d nodes" % len(nodes)

        if result == False:
            print '*** Could not find a path, no actions'
            print '\n'
            return []

        retActions = []
        initPos = result[0]
        prevPos = initPos
        for s in result:
            if s == initPos:
                continue
            (x,y) = prevPos[0]
            d = prevPos[1]
            states = [(x+neigh[d][0][0],y+neigh[d][0][1]),
                    (x+neigh[d][1][0],y+neigh[d][1][1]),
                    (x+neigh[d][2][0],y+neigh[d][2][1]),
                    (x+neigh[d][3][0],y+neigh[d][3][1])]
            #states = [(x,y+1),(x-1,y),(x,y-1),(x+1,y)] # u-0 l-1 d-2 r-3
            print '----------'
            print 'curPos:'
            print s
            print 'prev->nextStates:'
            print states
            if s[0] == states[0]:
                retActions = retActions + ['Forward']
            if s[0] == states[1]:
                retActions = retActions + ['TurnLeft','Forward']
            if s[0] == states[2]:
                retActions = retActions + ['TurnLeft','Forward']
            if s[0] == states[3]:
                retActions = retActions + ['TurnLeft','TurnLeft','Forward']

            prevPos = s
        #print '------------------------------------------'
        print 'path:'
        print result
        #print '------------------------------------------'
        print 'action sequence:'
        print retActions
        print '\n'
        return (retActions)


    def fcost(self, path):
        if len(path) > 0:
            endOfPath = path[-1]
            th1 = time()
            heuristic = self.problem.heuristic(endOfPath)
            th2 = time()
            self.timeOnHeuris = self.timeOnHeuris + (th2-th1)
            return len(path) - 1 + heuristic
        else:
            return 0

    def Astar(self):
        "Based on algorithm given in AI class"
        explored = set()
        initialPath = [self.problem.initialState]
        # Priority queue
        self.frontier.push(initialPath)
        while True:
            #print "*debug* numExplored = %d" % len(explored)
            if len(explored) > NMAX:
                return (False,NMAX)
            if self.frontier.isEmpty():
                return (False,len(explored))
            # This is the 'remove_choice' line from the algorithm
            path = self.frontier.pop()
            s = path[-1]
            explored.add(s[0])
            if self.problem.goalTest(s):
                return (path,len(explored))
            #(states, actions) = self.problem.nextStates(s)
            #for ind,ns in states.items():
            for ns in self.problem.nextStates(s):
                if ns[0] not in explored:
                    newPath = path + [ns]
                    self.frontier.push(newPath)
                    explored.add(ns[0])


