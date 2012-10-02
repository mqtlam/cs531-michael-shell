#!/usr/bin/env python

class Agent:
	"""The Agent class is an abstract class with useful constants."""
	FORWARD = 1
	RIGHT = 2
	LEFT = 3
	SUCK = 4
	OFF = 5

	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

	def takeStep(self, percept):
		"""Given a percept, determine and return an action."""
		[wall, dirt, home] = percept
		raise NotImplementedError("Implement by extending this class")
