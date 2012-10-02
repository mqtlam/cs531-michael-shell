#!/usr/bin/env python

class Agent:
	FORWARD = 1
	RIGHT = 2
	LEFT = 3
	SUCK = 4
	OFF = 5

	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

	def __init__(self):
		pass

	def takeStep(self, percept):
		[wall, dirt, home] = percept
		raise NotImplementedError("Implement by extending this class")
