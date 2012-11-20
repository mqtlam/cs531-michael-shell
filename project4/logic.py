import subprocess

class FluentLogic(object):
	"""
	Uses fluents to represent the wumpus world
	"""
	
	def query(self, query):
		"""
		Runs the given query, returning true if the query is true
		"""
		#start the process
		process = subprocess.Popen("./prover9", stdin=subprocess.PIPE,\
		stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		#give the process the body of logical rules and facts
		process.communicate(query)
		
		if process.returncode == 1:
			print query
			raise Exception("syntax error!")
		
		#prover 9 only exits with status 0 when the query was found to be true
		return process.returncode == 0

