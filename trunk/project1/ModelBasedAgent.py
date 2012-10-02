#!/usr/bin/env python
from Agent import *

class ModelBasedAgent(Agent):
	"""Deterministic model-based reflex agent with a small amount of memory."""
	state = 0

	def __init__(self):
		self.state = 0
	
	def takeStep(self, percept):
		[wall, dirt, home] = percept
		return Agent.OFF

