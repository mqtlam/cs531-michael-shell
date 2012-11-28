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
		self.KB = [] 
		self.KBString = ""

	def initWumpusWorldLogic(self):
		"""
		Adds Wumpus World logic to the KB. Only used for initialization.
		"""
		# wumpus world rules
		self.tell("all x all y all a all b Adjacent(Pos(x,y),Pos(a,b)) <-> (x = a & (y = b+(-1) | y = b+1)) | (y = b & (x = a+(-1) | x = a+1))") # adjacent definition
		self.tell("all s Breezy(s) <-> exists r Adjacent(r,s) & Pit(r)") # breezy & pit rule
		self.tell("all s Smelly(s) <-> exists r Adjacent(r,s) & Wumpus(r)") # smelly & wumpus rule
		self.tell("all t DeadWumpus(t+1) <-> ( Shoot(t) & ScreamAt(t+1) ) | DeadWumpus(t)") # dead wumpus successor-state axiom

		# successor-state axioms for agent properties
		self.tell("all t HaveArrow(t+1) <-> HaveArrow(t) & -Shoot(t)")
		self.tell("all t HaveGold(t+1) <-> (GlitterAt(t) & Grab(t)) | HaveGold(t)")

		# facts
		self.tell("Safe(Pos(0,0))") # square (0,0) is safe
		self.tell("HaveArrow(0)") # have arrow at time 0
		self.tell("-HaveGold(0)") # not have gold at time 0
		self.tell("DeadWumpus(0)") # wumpus is not dead at time 0
		self.tell("Location(Pos(0,0),0)") # agent's location is (0,0) at time 0
		self.tell("Facing(North,0)") # agent is facing north at time 0

	def constructProver9Query(self, query):
		"""
		Constructs a Prover-9 query by appending the knowledge base
		and ask query into Prover-9 format.
		"""
		assert(self.KBString != "" and query != "")

		result = "formulas(assumptions).\n\t" + \
			 self.KBString + \
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

	def tell(self, assertion):
		"""
		Performs a TELL query to the knowledge base.
		"""
		# coarse check for not adding duplicate logic rules
		if all(assertion not in l for l in self.KB):
			self.KBString += "\t" + assertion + ".\n"
			self.KB.append(assertion)

	def tellPercepts(self, percept, time):
		(breeze, stench, glitter, bump, scream) = percept
		if breeze:
			self.tell("BreezeAt("+str(time)+")")
		if stench:
			self.tell("StenchAt("+str(time)+")")
		if glitter:
			self.tell("GlitterAt("+str(time)+")")
		if bump:
			self.tell("BumpAt("+str(time)+")")
		if scream:
			self.tell("ScreamAt("+str(time)+")")

	def makeActionStatement(self, action, time):
		assert(action in ["Forward","TurnLeft","TurnRight","Shoot","Grab","Climb"])

		return action+"("+str(time)+")"
