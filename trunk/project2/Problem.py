#!/usr/bin/env python

class Problem:
	"""Problem represents a problem formulation of the Towers of Corvallis Problem. 
	   A state is represented as a list of strings where the three-element list 
	   represents the pegs and the strings represent the disks on the corresponding pegs.
	   A disk is labeled as an integer. Left-to-right string corresponds to top-to-bottom on the peg."""
	# Initial state
	initialState = ["","",""] 

	# Goal state
	# e.g. ["9876543210","",""]
	goalState = ["","",""] 

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
		newState = list(state)

		fromPeg = int(action[0])
		toPeg = int(action[1])

		[tmp, newState[fromPeg]] = [newState[fromPeg][0], newState[fromPeg][1:]]
		newState[toPeg] = tmp + newState[toPeg]
		
		return newState

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
