#!/usr/bin/env python

class SearchNode:
	"""SearchNode is a node of a search graph for problem solving."""
	# state in the state space to which the node corresponds
	state = None

	# node in search tree that generated this node
	parent = None

	# action that was applied to the parent to generate the node
	action = None

	# cost g(n) of the path from the initial state to the node, as indicated by parent pointers
	pathCost = 0

	# evaluation function value for this node: f(n) = g(n) + h(n)
	f = 0

	# heuristic function value for this node h(n)
	h = 0

	def __init__(self, state, parent, action, pathCost, h):
		self.state = state
		self.parent = parent
		self.action = action
		self.pathCost = pathCost
		self.h = h
		self.updateFValue()
	
	def updateFValue(self):
		self.f = self.pathCost + self.h
