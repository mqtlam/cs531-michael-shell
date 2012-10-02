#!/usr/bin/env python
from Agent import *

class ModelBasedAgent(Agent):
	"""Deterministic model-based reflex agent with a small amount of memory."""
	# 3 bits = 2^3 = up to 8 states
	state = 0

	def __init__(self):
		self.state = 0
	
	def takeStep(self, percept):
		[wall, dirt, home] = percept
		if self.state == 0 and dirt == 1:
			return Agent.SUCK
		if self.state == 0 and wall == 0:
			return Agent.FORWARD
		if self.state == 0 and wall == 1:
			self.state = 1
			return Agent.RIGHT
		if self.state == 1 and wall == 1:
			self.state = 6
			return Agent.RIGHT 
		if self.state == 1 and wall == 0:
			self.state = 2
			return Agent.FORWARD
		if self.state == 2:
			self.state = 3
			return Agent.RIGHT
		if self.state == 3 and dirt == 1:
			return Agent.SUCK
		if self.state == 3 and wall == 0:
			return Agent.FORWARD
		if self.state == 3 and wall == 1:
			self.state = 4
			return Agent.LEFT
		if self.state == 4 and wall == 1:
			self.state = 6
			return Agent.RIGHT
		if self.state == 4 and wall == 0:
			self.state = 5
			return Agent.FORWARD
		if self.state == 5:
			self.state = 0
			return Agent.LEFT
		if self.state == 6 and home == 1:
			return Agent.OFF
		if self.state == 6 and wall == 0:
			return Agent.FORWARD
		if self.state == 6 and wall == 1:
			return Agent.RIGHT
		raise NotImplementedError("Unreachable statement.")

