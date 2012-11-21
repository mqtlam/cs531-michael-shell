import random

import env

class LogicAgent(object):
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

		#load initial KB
		with open('./initKB.txt', 'r') as f:
			self.KB = f.read()
		
	def search(self, environment, logicEngine):
		"""
		Executes a logical search for the gold
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

			#get percepts
			(breeze, stench, glitter) = self.environ.sense(x,y)

			dead = self.environ.isDeadly(x,y) 

			if not dead:
				
				if glitter:
					goldFound = True
			
				else:
					
					#get a list of adjacent cells
					adjacentCells = self.environ.proxy(x,y)

					#here is a good place to ask a query to the logic engine....
					query = "B(0,0)."
					isQueryProved = self.kbAsk(query)

					#pick one randomly
					(x, y) = random.choice(adjacentCells)

				#increment the action counter
				self.actions += 1

		return (success, dead, self.actions, self.hasArrow)
	
	def kbTell(self, assertions):
		self.KB += assertions

	def kbAsk(self, query):
		q = "formulas(goals).\n"
		q += query 
		q += "\nend_of_list."
		return self.logic.query(self.KB + "\n" + q)
