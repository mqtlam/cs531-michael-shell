class KnowledgeBase(object):
	"""
	Knowledge Base that the logic agent uses.
	"""

	def __init__(self, logicEngine, environ):
		"""
		Initializes the knowledge base.
		"""
		self.logic = logicEngine
		self.environ = environ
		self.worldSize = environ.size

		#list of assertions in Prover-9 format each ending in '.'
		self.KBAssumptions = [] 
		self.KBAssumptionsString = ""

		self.KBUsable = []
		self.KBUsableString = ""

	def initWumpusWorldLogic(self):
		"""
		Adds Wumpus World logic to the KB. Only used for initialization.
		"""
		#self.tell("")

	def constructProver9Query(self, query):
		"""
		Constructs a Prover-9 query by appending the knowledge base
		and ask query into Prover9 format.
		"""
		assert(self.KBAssumptionsString != "" and self.KBUsableString != "" and query != "")

		result = "formulas(usable).\n" + \
			 self.KBUsableString + \
			 "end_of_list.\n\n" + \
			 "formulas(assumptions).\n" + \
			 self.KBAssumptionsString + \
			 "end_of_list.\n\n" + \
			 "formulas(goals).\n\t" + \
			 query + ".\n" + \
			 "end_of_list.\n"

		# debug...
		with open("./kb.txt", 'w') as f:
			f.write(result)

		return result

	def ask(self, query):
		"""
		Performs an ASK query to the knowledge base.
		"""
		fullQuery = self.constructProver9Query(query)
		result =  self.logic.query(fullQuery)

		# cache proven results
		if result:
			self.tell(query)

		return result

	def tell(self, assertion, usable = False):
		"""
		Performs a TELL query to the knowledge base.
		"""
		# coarse check for not adding duplicate logic rules
		if usable:
			if all(assertion not in l for l in self.KBUsable):
				self.KBUsableString += "\t" + assertion + ".\n"
				self.KBUsable.append(assertion)
		else:
			if all(assertion not in l for l in self.KBAssumptions):
				self.KBAssumptionsString += "\t" + assertion + ".\n"
				self.KBAssumptions.append(assertion)

	def tellAssumptionsAtTime(self, percept, time, current, hasArrow):
		# tell percepts
		(breeze, stench, glitter, bump, scream) = percept
		if breeze:
			self.tell("Breeze(%d)" % time)
			self.tell("B(%d,%d)" % current)
		else:
			self.tell("-Breeze(%d)" % time)
			self.tell("-B(%d,%d)" % current)
		if stench:
			self.tell("Stench(%d)" % time)
			self.tell("S(%d,%d)" % current)
		else:
			self.tell("-Stench(%d)" % time)
			self.tell("-S(%d,%d)" % current)
		if glitter:
			self.tell("Glitter(%d)" % time)
			self.tell("G(%d,%d)" % current)
		else:
			self.tell("-Glitter(%d)" % time)
			self.tell("-G(%d,%d)" % current)
		if bump:
			self.tell("Bump(%d)" % time)
		else:
			self.tell("-Bump(%d)" % time)
		if scream:
			self.tell("Scream(%d)" % time)
		else:
			self.tell("-Scream(%d)" % time)

		# tell if wumpus is alive TODO
		#self.tell("WumpusAlive(0)")

		# tell current location and safe
		self.tell("Loc(%d,%d,%d)" % (current[0], current[1], time))
		self.tell("OK(%d,%d,%d)" % (current[0], current[1], time))

		# tell if has arrow
		if hasArrow:
			self.tell("HaveArrow(%d)" % time)
		else:
			self.tell("-HaveArrow(%d)" % time)

	def tellUsableAtTime(self, time, current):
		# Adjacent logic
		adjacentCells = self.environ.proxy(current[0], current[1])
		Pstring = ' | '.join(["P(%d,%d)" % c for c in adjacentCells])
		Wstring = ' | '.join(["W(%d,%d)" % c for c in adjacentCells])
		self.tell(("B(%d,%d) <-> " % current) + Pstring, True)
		self.tell(("S(%d,%d) <-> " % current) + Pstring, True)

		# Location logic
		self.tell("Loc(%d,%d,%d) -> (Breeze(%d) <-> B(%d,%d))" % (current[0], current[1], time, time, current[0], current[1]), True)
		self.tell("Loc(%d,%d,%d) -> -P(%d,%d)" % (current[0], current[1], time, current[0], current[1]), True)
		self.tell("Loc(%d,%d,%d) -> (Stench(%d) <-> W(%d,%d))" % (current[0], current[1], time, time, current[0], current[1]), True)
		self.tell("Loc(%d,%d,%d) ->(-W(%d,%d)) | (W(%d,%d) & -WumpusAlive(%d))" % (current[0], current[1], time, current[0], current[1], current[0], current[1], time), True)
		self.tell("Loc(%d,%d,%d) & G(%d,%d) -> Grab(%d)" % (current[0], current[1], time, current[0], current[1], time))
		
		# OK logic
		for x in range(self.worldSize):
			for y in range(self.worldSize):
				self.tell("OK(%d,%d,%d) <-> -P(%d,%d) & -(W(%d,%d) & WumpusAlive(%d))" % (x,y,time,x,y,x,y,time), True)	

	def makeActionStatement(self, action, time):
		assert(action in ["Forward","TurnLeft","TurnRight","Shoot","Grab","Climb"])

		return action+"("+str(time)+")"
