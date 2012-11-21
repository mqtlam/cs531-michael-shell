class KnowledgeBase(object):
	"""
	Knowledge Base that the logic agent uses.
	"""

	def __init__(self, logicEngine):
		"""
		Initializes the knowledge base.
		"""
		self.logic = logicEngine
		with open('./initKB.txt', 'r') as f:
			self.KB = f.read()

	def ask(self, query):
		"""
		Performs an ASK query to the knowledge base.
		"""
		q = "formulas(goals).\n"
		q += query
		q += "\nend_of_list."
		return self.logic.query(self.KB + "\n" + q)

	def tell(self, assertions):
		"""
		Performs a TELL query to the knowledge base.
		"""
		self.KB += assertions

