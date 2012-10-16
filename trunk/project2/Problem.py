#!/usr/bin/env python

class Problem:
	"""Problem represents a problem formulation of the Towers of Corvallis Problem. 
	   A state is represented as a list of lists where the outer three-element list 
	   represents the pegs and the inner lists represent the disks on the corresponding pegs.
	   A disk is labeled as an integer. Left-to-right of a peg list corresponds to top-to-bottom on a peg."""
	# Initial state
	initialState = ([], [], []) 

	# Goal state
	# e.g. [[9,8,7,6,5,4,3,2,1,0],[],[]]
	goalState = ([], [], [])

	def __init__(self, initialState, goalState):
		self.initialState = initialState
		self.goalState = goalState

	def initialState(self):
		"""Return the initial state."""
		return initialState

	def actions(self, state):
		"""Returns a list of allowable actions given a state. 
		   Actions are represented as a string of two numbers, 
		   the first number being the peg to pop and the second 
		   number being the peg to push. 3 pegs: 0, 1, 2"""
		lst = []
		if len(state[0]) > 0:
			lst.extend(["01","02"])
		if len(state[1]) > 0:
			lst.extend(["10","12"])
		if len(state[2]) > 0:
			lst.extend(["20","21"])
		return lst 

	def result(self, state, action):
		"""Compute and return the new state given a current state and action."""
		newState = (list(state[0]), list(state[1]), list(state[2])) # new lists, not same pointers!
		tmp = newState[int(action[0])].pop(0)
		newState[int(action[1])].insert(0, tmp)
		return newState

	# TODO: make more efficient?
	def goalTest(self, state):
		"""Returns true if the given state matches the goal state."""
		for curr, goal in zip(state, self.goalState):
			if len(curr) != len(goal):
				return False
			for a, b in zip(curr, goal):
				if a != b:
					return False
		print "Goal found"
		return True
		
	def stepCost(self, state, action):
		"""Returns the step cost given the state x action."""
		return 1 

	def heuristic(self, state, heuristicType):
		"""Evaluates a heuristic function. Specify type of heuristic to use."""
		if heuristicType == 1:
			return self.heuristicFunction1(state)
		elif heuristicType == 2:
			return self.heuristicFunction2(state)
		else:
			return 0

	def heuristicFunction1(self, state):
		"""Returns the heuristic function value evaluated at current state."""
		value = 0
		for curr, goal in zip(state, self.goalState):
			for a, b in zip(curr, goal):
				if a == b:
					value += 1	
		return value

	def heuristicFunction2(self, state):
		"""Returns the heuristic function value evaluated at current state."""
		return 0
