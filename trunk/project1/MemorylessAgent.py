#!/usr/bin/env python
from Agent import *

class MemorylessAgent(Agent):
	def __init__(self):
		pass

	def takestep(self, percept):
		[wall, dirt, home] = percept
		# implement
		return Agent.OFF	

