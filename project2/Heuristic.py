#!/usr/bin/env python

class Heuristic:
	"""Heuristic is a class that stores a heuristic function for a particular Problem instance.
	   This class contains the two heuristics: admissible and non-admissible."""
    #goalState = ["","",""]
    #heuristicType = 0

	def __init__(self, heuristicType, goalState):
		self.heuristicType = heuristicType
		self.goalState = goalState

	def h(self, state):
		"""Evaluates a heuristic function. Specify type of heuristic to use."""
		if self.heuristicType == 1:
			return self.heuristicFunction1(state)
		elif self.heuristicType == 2:
			return self.heuristicFunction2(state)
		elif self.heuristicType == 3:
			return self.heuristicFunction3(state)
		elif self.heuristicType == 4:
			return self.heuristicFunction4(state)
		else:
			return 0 # no heuristic

	def heuristicFunction1(self, state):
		"""Returns the heuristic function value evaluated at current state."""
		return state.numDisksInPeg(0)

	def heuristicFunction2(self, state):
		"""Returns the heuristic function value evaluated at current state."""
		value = len(self.goalState[0])
		testState = "x"*(value-len(state[0])) + state[0]
		for a, b in zip(testState, self.goalState[0]):
			if a == b:
				value -= 1
		return value

	def heuristicFunction3(self, state):
		"""Returns the heuristic function value evaluated at current state."""
		value = 2*len(self.goalState[0])
		testState = state[0]
		streak = True
		for a, b in zip(reversed(testState), reversed(self.goalState[0])):
			if a == b:
				value -= 1
				if streak:
					value -= 1
			elif streak:
				streak = False
		return value
	def heuristicFunction4(self, state):
		"""Returns the heuristic function value evaluated at current state."""
        	h = 0
        	for i,s in enumerate(state.pegs[0]):
            		h = h + abs(self.goalState[0][i]-s)
        	h = h + state.numDisksInPeg(1)
        	h = h + state.numDisksInPeg(2)
		return h
