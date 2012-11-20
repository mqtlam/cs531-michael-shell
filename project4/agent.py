import random

import env

class RandomAgent(object):
	"""
	A hybrid agent that uses logic and a planner to work its way through the
	wumpus world
	"""
	
	def __init__(self):
		"""
		Initializes the agent
		"""
		self.logic = None
		self.environ = None
		self.actions = 0
		self.hasArrow = True
		
	def search(self, environment, logicEngine):
		"""
		Executes a random search for the gold
		"""
		self.environ = environment
		self.logic = logicEngine
		self.actions = 0
		self.hasArrow = True
		success = False
		dead = False
		goldFound = False
		x, y = (0,0)
	
		#keep looking for the gold stupidly
		while not goldFound and not dead:

			(breeze, stench, gilter) = self.environ.sense(x,y)

			dead = self.environ.isDeadly(x,y) 

			if not dead:
				
				if gilter:
					goldFound = True
			
				else:
					
					#get a list of adjacent cells
					adjacentCells = self.environ.proxy(x,y)

					#here is a good place to ask a query to the logic engine....
					#self.logic.query( .... )

					#pick one randomly
					(x, y) = random.choice(adjacentCells)

				#increment the action counter
				self.actions += 1

		return (success, dead, self.actions, self.hasArrow)
	
