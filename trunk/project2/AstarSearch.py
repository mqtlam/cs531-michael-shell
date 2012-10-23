#!/usr/bin/env python
from AstarProblem import *
from Heuristic import *
#import heapq
from util import PriorityQueueWithFunction
from time import *

NMAX = 10000000

class AstarSearch:
    def __init__(self):
        self.numExpandedNodes = 0
        self.heuristic = None
        self.frontier = PriorityQueueWithFunction(self.fcost)
        self.timeOnHeuris = 0
        self.timeOnTotal = 0

    def run(self, problem, heuristicType = 0):
        """Runs the Astar algorithm on a problem and heuristic, and returns a solution or failure."""
        self.heuristic = Heuristic(heuristicType, problem.goalState)
        #h = self.heuristic.h(problem.initialState)

        t1 = time()
        (result,nNodes) = self.Astar(problem)
        t2 = time()
        self.timeOnTotal = t2 - t1
        #print "Explored %d nodes" % len(nodes)
        return (result, nNodes)

    def fcost(self, path):
        if len(path) > 0:
            endOfPath = path[-1]
            th1 = time()
            heuristic = self.heuristic.h(endOfPath)
            th2 = time()
            self.timeOnHeuris = self.timeOnHeuris + (th2-th1)
            return len(path) - 1 + heuristic
        else:
            return 0

    def Astar(self, problem):
        "Based on algorithm given in AI class"
        explored = set()
        initialPath = [problem.initialState]
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
            explored.add(s)
            if problem.goalTest(s):
                return (path,len(explored))
            for ns in problem.nextStates(s):
                if ns not in explored:
                    newPath = path + [ns]
                    self.frontier.push(newPath)
                    explored.add(ns)


