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
		elif self.heuristicType == 5:
			return self.heuristicFunction5(state)
		elif self.heuristicType == 6:
			return self.heuristicFunction6(state)
		elif self.heuristicType == 7:
			return self.heuristicFunction7(state)
		elif self.heuristicType == 8:
			return self.heuristicFunction8(state)
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

	def heuristicFunction5(self, state):
		"""Returns the heuristic function value evaluated at current state."""
        	h = 0
		goalStateReversed = list(reversed(self.goalState[0]))
        	for i,s in enumerate(reversed(state[0])):
            		h = h + abs(int(goalStateReversed[i])-int(s))
        	h = h + len(state[1])
        	h = h + len(state[2])
		return h

	def heuristicFunction6(self, state):
		"""Returns the heuristic function value evaluated at current state."""
        	h = 0
        	for i,s in enumerate(state.pegs[0]):
            		h = h + abs(self.goalState[0][i]-s)*2
        	h = h + state.numDisksInPeg(1)*2
        	h = h + state.numDisksInPeg(2)*2
		return h
	def heuristicFunction7(self, state):
		"""Returns the heuristic function value evaluated at current state."""
        	h = 0
        	hh = [0]
            	for i,s in enumerate(state.pegs[0]):
                	hh.append(abs(self.goalState[0][i]-s))
        	h = h + max(hh)
        	h = h + state.numDisksInPeg(1)
        	h = h + state.numDisksInPeg(2)
		return h
	def heuristicFunction8(self, state):
		"""Returns the heuristic function value evaluated at current state."""
        	h = 0
		goalStateReversed = list(reversed(self.goalState[0]))
        	for i,s in enumerate(reversed(state[0])):
            		h = h + abs(int(goalStateReversed[i])-int(s))*2
        	h = h + len(state[1])*2
        	h = h + len(state[2])*2
		return h
