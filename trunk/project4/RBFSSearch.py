#!/usr/bin/env python
from Problem import *
from SearchNode import *
#from Heuristic import *
from time import *

neigh = [
        [(0,1),(-1,0),(1,0),(0,-1)], # 0 = u
        [(1,0),(0,1),(0,-1),(-1,0)], # 1 = r
        [(0,-1),(1,0),(-1,0),(0,1)], # 2 = d
        [(-1,0),(0,-1),(0,1),(1,0)], # 3 = l
        ]

class RBFSProblem:
	def __init__(self, initialState, goalState, allowed):
		self.initialState = initialState #[(x,y),d]
		self.goalState = goalState #[x,y]
		self.map = allowed #list of squares

	def initialState(self):
		"""Return the initial state."""
		return initialState

        def isAllowed(self,square):
                try:
                        ind = self.map.index(square)
                except ValueError:
                        ind = -1
                if ind == -1:
                        return False
                else:
                        return True

	def actions(self, state):
		"""possible neighbours in allowed squares"""
                (x,y) = state[0]
                nStates = [(x,y+1),(x+1,y),(x,y-1),(x-1,y)] # u-0 r-1 d-2 l-3
                lst = []
                for i,s in enumerate(nStates):
                        if self.isAllowed(s) == True:
                                lst.append(i)
                                #retStates = retStates + [[s,i]]
		#lst = [0,1,2,3]		
		return lst 

	def result(self, state, action):
		"""Compute and return the new state given a current state and action."""
		(x,y) = state[0]
                nStates = [(x,y+1),(x+1,y),(x,y-1),(x-1,y)] # u-0 r-1 d-2 l-3
                newState = [nStates[action],action]
		return newState

	def goalTest(self, state):
                for gs in self.goalState:
                        if state[0] == gs:
                                return True
                return False
		
	def stepCost(self, state, action):
		"""Returns the step cost given the state x action."""
		return 1 

        def heuristic(self,current):
                "without considering direction"
                "minimum block dist(current, goalState[i])"
                (x,y) = current[0]
                minDist = -1
                for g in self.goalState:
                        (xg,yg) = g
                        dist = abs(xg-x) + abs(yg-y)
                        if  dist < minDist:
                                minDist = dist
                return minDist

class RBFSSearch:
	"""RBFSSearch performs RBFS search."""
	INFINITY = float("inf")
	NMAX = 100

	def __init__(self,problem,shoot):
		self.numExpandedNodes = 0
		#self.heuristic = None
        	self.timeOnHeuris = 0
        	self.timeOnTotal = 0
                self.problem = problem
                self.shoot = shoot

	def run(self):
		"""Runs the RBFS algorithm on a problem and heuristic, and returns a solution or failure."""

                if self.problem.goalState == []:
                        print '*** No goals, no actions'
                        print '\n'
                        return []

        	t1 = time()
		(result, fvalue) = self.RBFS(self.makeNode(self.problem.initialState, self.problem.heuristic(self.problem.initialState)), self.INFINITY)
        	t2 = time()
        	self.timeOnTotal = t2 - t1

                if result == False or result == []:
                        print '*** Could not find a path, no actions'
                        print '\n'
                        return []

		if self.exceedsNMAX():
			print "Terminated after NMAX expansions."
		#print "Num Expansions: ", self.numExpandedNodes

                rStates = []
                for node in result:
                        rStates.append(node.state)
                print "-------------------"
                print "states:"
                print rStates
		
                retActions = []
                initPos = rStates[0]
                prevPos = initPos
                for s in rStates:
                        if s == initPos:
                                continue
                        (x,y) = prevPos[0]
                        d = prevPos[1]
                        states = [(x+neigh[d][0][0],y+neigh[d][0][1]),
                            (x+neigh[d][1][0],y+neigh[d][1][1]),
                            (x+neigh[d][2][0],y+neigh[d][2][1]),
                            (x+neigh[d][3][0],y+neigh[d][3][1])]

                        if s[0] == states[0]:
                                retActions = retActions + ['Forward']
                        if s[0] == states[1]:
                                retActions = retActions + ['TurnLeft','Forward']
                        if s[0] == states[2]:
                                retActions = retActions + ['TurnRight','Forward']
                        if s[0] == states[3]:
                                retActions = retActions + ['TurnLeft','TurnLeft','Forward']
                        prevPos = s

                if self.shoot == True:
                        retActions.insert(-2,'Shoot')

        
                print 'path:'
                print rStates

                print 'action sequence:'
                print retActions
                print '\n'
                return (retActions)

	def RBFS(self, node, fLimit):
		"""Returns a solution, or failure and a new f-cost limit."""
		if self.exceedsNMAX():
			return ([], 0)
		if self.problem.goalTest(node.state):
			return (self.solution(node), 0)
		successors = []
		for action in self.problem.actions(node.state):
            		th1 = time()
			#h = self.heuristic.h(node.state)
                        h = self.problem.heuristic(node.state)
            		th2 = time()
            		self.timeOnHeuris = self.timeOnHeuris + (th2-th1)
			successors.append(self.childNode(node, action, h))
		if not successors:
			return (False, self.INFINITY)
		for s in successors:
			s.f = max(s.pathCost + s.h, node.f)
		while True:
			[best, alternative] = self.getFirstSecondLowest(successors)
			if best.f > fLimit:
				return (False, best.f)
                        if alternative == None:
                                [result, best.f] = self.RBFS(best, fLimit)  
                        else:      
			        [result, best.f] = self.RBFS(best, min(fLimit, alternative.f))
			if result != False:
				return (result, best.f)

	def makeNode(self, initialState, heuristic):
		"""Constructs a node, used for the initial state."""
		self.updateNMAX()
		return SearchNode(initialState, None, None, 0, heuristic)

	def solution(self, node):
		"""Return a solution path by tracing back to the initial state."""
		lst = []
		curr = node
		while curr is not None:
			lst.append(curr)
			curr = curr.parent
		lst.reverse()
		return lst

	def childNode(self, parent, action, heuristic):
		"""Construct a child node."""
		self.updateNMAX()
		state = self.problem.result(parent.state, action)
		pathCost = parent.pathCost + self.problem.stepCost(parent.state, action)
		return SearchNode(state, parent, action, pathCost, heuristic)

	def getFirstSecondLowest(self, lst):
		"""Get the first and second lowest f-valued element.
		   If the list only has one element, the alternative is None."""
		if len(lst) < 1:
			raise ValueError("lst must have at least one element")
		elif len(lst) == 1:
			return [lst[0], None]
		else:
			lst = sorted(lst, key=lambda s: s.f)
			return [lst[0], lst[1]]

	def updateNMAX(self):
		self.numExpandedNodes += 1

	def exceedsNMAX(self):
		return self.numExpandedNodes >= self.NMAX

