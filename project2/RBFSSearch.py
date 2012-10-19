#!/usr/bin/env python
from Problem import *
from SearchNode import *
from Heuristic import *

class RBFSSearch:
	"""RBFSSearch performs RBFS search."""
	INFINITY = float("inf")
	NMAX = 42000000
	
	numExpandedNodes = 0
	heuristic = None

	def __init__(self):
		self.numExpandedNodes = 0
		self.heuristic = None

	def run(self, problem, heuristicType = 0):
		"""Runs the RBFS algorithm on a problem and heuristic, and returns a solution or failure."""
		self.heuristic = Heuristic(heuristicType, problem.goalState)
		h = self.heuristic.h(problem.initialState)

		[result, fvalue] = self.RBFS(problem, self.makeNode(problem.initialState, h), self.INFINITY)

		if self.exceedsNMAX():
			print "Terminated after NMAX expansions."
		print "Num Expansions: ", self.numExpandedNodes
		return result

	def RBFS(self, problem, node, fLimit):
		"""Returns a solution, or failure and a new f-cost limit."""
		if self.exceedsNMAX():
			return [self.solution(node), 0]
		if problem.goalTest(node.state):
			return [self.solution(node), 0]
		successors = []
		for action in problem.actions(node.state):
			h = self.heuristic.h(node.state)
			successors.append(self.childNode(problem, node, action, h))
		if not successors:
			return [False, self.INFINITY]
		for s in successors:
			s.f = max(s.pathCost + s.h, node.f)
		while True:
			[best, alternative] = self.getFirstSecondLowest(successors)
			if best.f > fLimit:
				return [False, best.f]
			[result, best.f] = self.RBFS(problem, best, min(fLimit, alternative.f))
			if result != False:
				return [result, best.f]

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

	def childNode(self, problem, parent, action, heuristic):
		"""Construct a child node."""
		self.updateNMAX()
		state = problem.result(parent.state, action)
		pathCost = parent.pathCost + problem.stepCost(parent.state, action)
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

