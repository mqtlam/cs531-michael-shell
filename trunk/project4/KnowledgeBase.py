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

	def initWumpusWorldLogic(self):
		"""
		Adds Wumpus World logic to the KB. Only used for initialization.
		"""
		# wumpus world rules
		self.tell("all x all y all a all b Adjacent(Pos(x,y),Pos(a,b)) <-> (x = a & (y = b+(-1) | y = b+1)) | (y = b & (x = a+(-1) | x = a+1))") # adjacent definition
		self.tell("all s Breezy(s) <-> exists r Adjacent(r,s) & Pit(r)") # breezy & pit rule
		self.tell("all s Smelly(s) <-> exists r Adjacent(r,s) & Wumpus(r)") # smelly & wumpus rule
		self.tell("all t DeadWumpus(t+1) <-> ( Action(Shoot,t) & ScreamAt(t+1) ) | DeadWumpus(t)") # dead wumpus successor-state axiom

		# successor-state axioms for agent properties
		self.tell("all t HaveArrow(t+1) <-> HaveArrow(t) & -Action(Shoot, t)")
		self.tell("all t HaveGold(t+1) <-> (GlitterAt(t) & Action(Grab, t)) | HaveGold(t)")
		self.tell("all t Facing(North,t+1) <-> ( (Facing(West,t) & Action(TurnRight, t)) | (Facing(East,t) & Action(TurnLeft,t)) ) | ( Facing(North,t) & -(Action(Right,t) & Action(Left,t)))")
		self.tell("all t Facing(East,t+1) <-> ( (Facing(North,t) & Action(TurnRight, t)) | (Facing(South,t) & Action(TurnLeft,t)) ) | ( Facing(East,t) & -(Action(Right,t) & Action(Left,t)))")
		self.tell("all t Facing(South,t+1) <-> ( (Facing(East,t) & Action(TurnRight, t)) | (Facing(West,t) & Action(TurnLeft,t)) ) | ( Facing(South,t) & -(Action(Right,t) & Action(Left,t)))")
		self.tell("all t Facing(West,t+1) <-> ( (Facing(South,t) & Action(TurnRight, t)) | (Facing(North,t) & Action(TurnLeft,t)) ) | ( Facing(West,t) & -(Action(Right,t) & Action(Left,t)))")
		self.tell("all t all i all j Location(Pos(i,j),t+1) <-> ( Location(Pos(i,j),t) & (-Action(Forward,t) | BumpAt(t)) ) | ( Location(Pos(i,j+(-1)),t) & (Facing(North,t) & Action(Forward,t)) ) | ( Location(Pos(i+(-1),j),t) & (Facing(East,t) & Action(Forward,t)) ) | ( Location(Pos(i,j+1),t) & (Facing(South,t) & Action(Forward,t)) ) | ( Location(Pos(i+1,j),t) & (Facing(North,t) & Action(Forward,t)) )")

		# perception rules
		#self.tell("all t all s all g all m all c Percept(Breeze,s,g,m,c,t) -> BreezeAt(t)")
		#self.tell("all t all b all g all m all c Percept(b,Stench,g,m,c,t) -> StenchAt(t)")
		#self.tell("all t all b all s all m all c Percept(b,s,Glitter,m,c,t) -> GlitterAt(t)")
		#self.tell("all t all b all s all g all c Percept(b,s,g,Bump,c,t) -> BumpAt(t)")
		#self.tell("all t all b all s all g all m Percept(b,s,g,m,Scream,t) -> ScreamAt(t)")

		# facts
		self.tell("Safe(Pos(1,1))") # square (1,1) is safe
		self.tell("HaveArrow(1)") # have arrow at time 1
		self.tell("-HaveGold(1)") # not have gold at time 1
		self.tell("DeadWumpus(1)") # wumpus is not dead at time 1
		self.tell("Location(Pos(1,1),1)") # agent's location is (1,1) at time 1
		self.tell("Facing(North,1)") # agent is facing north at time 1

	def constructProver9Query(self, query):
		"""
		Constructs a Prover-9 query by appending the knowledge base
		and ask query into Prover-9 format.
		"""
		assert(self.KB != [] and query != "")

		result = "set(production).\n\n" + \
			 "formulas(assumptions).\n\t" + \
			 ".\n\t".join(self.KB) + '.\n' + \
			 "end_of_list.\n\n" + \
			 "formulas(goals).\n\t" + \
			 query + ".\n" + \
			 "end_of_list.\n"
		return result

	def ask(self, query):
		"""
		Performs an ASK query to the knowledge base.
		"""
		fullQuery = self.constructProver9Query(query)
		result =  self.logic.query(fullQuery)
		print result
		return result

	def tell(self, assertion):
		"""
		Performs a TELL query to the knowledge base.
		"""
		#course check for not adding duplicate logic rules
		if all(assertion not in l for l in self.KB):
			self.KB.append(assertion)

	def makePerceptStatement(self, percept, time):
		breeze = "Breeze" if percept[0] else "None"
		stench = "Stench" if percept[1] else "None"
		glitter = "Glitter" if percept[2] else "None"
		return "Percept("+breeze+","+stench+","+glitter+","+str(time)+")"

	def makeActionStatement(self, action, time):
		return "Action("+action+","+str(time)+")"
