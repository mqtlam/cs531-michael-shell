#!/usr/bin/env python
from AstarProblem import *
from Heuristic import *
#import heapq
from util import PriorityQueueWithFunction

class AstarSearch:
    def __init__(self):
        self.numExpandedNodes = 0
        self.heuristic = None
        self.frontier = PriorityQueueWithFunction(self.fcost)

    def run(self, problem, heuristicType = 0):
        """Runs the Astar algorithm on a problem and heuristic, and returns a solution or failure."""
        self.heuristic = Heuristic(heuristicType, problem.goalState)
        #h = self.heuristic.h(problem.initialState)

        result = self.Astar(problem)
        return result

    def fcost(self, path):
        if len(path) > 0:
            endOfPath = path[-1]
            heuristic = self.heuristic.h(endOfPath)
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
            if self.frontier.isEmpty():
                return False
            # This is the 'remove_choice' line from the algorithm
            path = self.frontier.pop()
            s = path[-1]
            explored.add(s)
            if problem.goalTest(s):
                return path
            for ns in problem.nextStates(s):
                if ns not in explored:
                    newPath = path + [ns]
                    self.frontier.push(newPath)
                    explored.add(ns)


