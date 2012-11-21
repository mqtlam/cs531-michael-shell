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

	def constructProver9Query(self, query):
		assert(self.KB != [] and query != "")

		result = "set(production).\n" + \
			 "formulas(assumptions).\n " + \
			 ".\n ".join(self.KB) + '.\n' + \
			 "end_of_list.\n" + \
			 "formulas(goals).\n " + \
			 query + ".\n" + \
			 "end_of_list.\n"
		return result

	def ask(self, query):
		"""
		Performs an ASK query to the knowledge base.
		"""
		fullQuery = self.constructProver9Query(query)
		result =  self.logic.query(fullQuery)
		return result

	def tell(self, assertion):
		"""
		Performs a TELL query to the knowledge base.
		"""
		if type(assertion) is list:
			self.KB.extend(assertion)
		elif type(assertion) is str:
			self.KB.append(assertion)

	def makePerceptStatement(self, percept, time):
		pass
