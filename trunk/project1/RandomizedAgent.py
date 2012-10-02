#!/usr/bin/env python
from Agent import *

class RandomizedAgent(Agent):
	def __init__(self):
		pass

	def takeStep(self, percept):
		[wall, dirt, home] = percept
		# implement
		return Agent.OFF	

