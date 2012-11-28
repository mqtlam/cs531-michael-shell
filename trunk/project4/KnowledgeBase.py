class KnowledgeBase(object):
	"""
	Knowledge Base that the logic agent uses.
	"""

	def __init__(self, logicEngine):
		"""
		Initializes the knowledge base.
		"""
		self.logic = logicEngine

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

		result = "formulas(usable).\n\t" + \
			 self.KBUsableString + \
			 "end_of_list.\n\n" + \
			 "formulas(assumptions).\n\t" + \
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

	def tellPercepts(self, percept, time, current):
		(breeze, stench, glitter, bump, scream) = percept
		if breeze:
			self.tell("Breeze(%d)" % time)
			self.tell("B(%d,%d)" % current)
		if stench:
			self.tell("Stench(%d)" % time)
			self.tell("S(%d,%d)" % current)
		if glitter:
			self.tell("Glitter(%d)" % time)
		if bump:
			self.tell("Bump(%d)" % time)
		if scream:
			self.tell("Scream(%d)" % time)

	def makeActionStatement(self, action, time):
		assert(action in ["Forward","TurnLeft","TurnRight","Shoot","Grab","Climb"])

		return action+"("+str(time)+")"
