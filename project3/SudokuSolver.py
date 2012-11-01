#!/usr/bin/env python
from time import clock, time
from random import choice

class SudokuSolver:
	"""The Sudoku class represents a sudoku board."""

	def __init__(self, useRandomUnassignedVariable = False):
		"""Initialize the Sudoku board and CSP formulation."""

		### Initialize variables
		self.resetVariables()

		### Options
		self.useRandomUnassignedVariable = useRandomUnassignedVariable

	def resetVariables(self):
		### Sudoku board construction
		self.rows = "123456789"
		self.cols = "abcdefghi"
		self.squares = [i+j for i in self.rows for j in self.cols]

		### Sudoku CSP formulation

		# domain of all squares
		self.domain = "123456789"

		# maps each square to available domain represented as a string
		self.variables = dict((s, self.domain) for s in self.squares)

		# list of alldiff constraints
		self.alldiffs = ([[i+j for i in self.rows for j in c] for c in self.cols] +
				[[i+j for i in r for j in self.cols] for r in self.rows] +
				[[i+j for i in r for j in c] for r in ['123','456','789'] for c in ['abc','def','ghi']])

		# maps each square to a set of squares affected by it (should have 20 affected squares per square)
		self.neighbors = dict((s, list(set(sum([i for i in self.alldiffs if s in i],[]))-set([s]))) for s in self.squares)

		### Variables to keep track of statistics
		self.numBacktrackings = 0
		self.numRuleTwo = 0
		self.numFilledIn = 0
		self.solved = None

	def setup(self, board):
		"""Initializes the board configuration to board."""
		# reset variables
		self.resetVariables()

		# set up board
		for i, digit in enumerate(board):
			index = '' + self.rows[i/9] + self.cols[i%9]
			if digit != "0":
				self.variables[index] = digit
				self.numFilledIn += 1

	def solve(self):
		"""Attempts to solve the current board."""
		if self.solved is not None:
			return self.solved

		startClock = time()
		self.variables = self.backtrackSearch(self.variables)
		endClock = time()

		self.solved = [self.isSolved(self.variables), self.numBacktrackings, self.numRuleTwo, self.numFilledIn, endClock - startClock]
		return self.solved 

	def isSolved(self, variables):
		"""Returns true if the current board is solved."""
		for square in self.variables:
			if len(variables[square]) != 1:
				return False
			"""for neighbor in self.neighbors[square]:
				if len(variables[neighbor]) != 1:
					return False
				elif variables[neighbor] == variables[square]:
					return False"""
		return True

	def printBoard(self, variables = None):
		"""Prints the current board. For debugging purposes."""
		if variables is None:
			variables = self.variables

		print "  a b c   d e f   g h i"
		for r in self.rows:
			print r, ''.join((variables[r+c] if len(variables[r+c]) == 1 else '-')+' '+('| ' if c in 'cf' else '') for c in self.cols)
			if r in '36':
				print ' ' + '-'*23
		print

	def printFullBoard(self, variables = None):
		"""Prints the current board, complete with the domain for each variable. For debugging purposes."""
		if variables is None:
			variables = self.variables
		
		width = 1+max(len(variables[s]) for s in self.squares)
		print '  ' + ''.join(c.center(width)+('  ' if c in 'cf' else '') for c in "abcdefghi")
		for r in self.rows:
			print r, ''.join(variables[r+c].center(width)+('| ' if c in 'cf' else '') for c in self.cols)
			if r in '36':
				print ' -' + '-'.join(['-'*(width*3)]*3)
		print

	### CSP Functions

	def constraintPropagation(self, variables):
		"""Perform constraint propagation by assigning consistent values. 
		Return updated domains for variables or False upon contradiction."""
		changed = True
		while changed:
			changed = False

			# (rule 1) - implicit in representation

			# (rule 2)
			(variables, changed) = self.ruleTwo(variables, changed)

			# (rule 3) - naked triples
			(variables, changed) = self.nakedK(2, variables, changed)
			(variables, changed) = self.nakedK(3, variables, changed)

			# propagation step
			for square in variables:
				values = variables[square]
				# if no candidates left, then contradiction
				if len(values) == 0:
					return False

				# if exactly one candidate, then propagate
				elif len(values) == 1:
					for neighbor in self.neighbors[square]:
						if values in variables[neighbor]:
							variables[neighbor] = variables[neighbor].replace(values,'')
							changed = True
		return variables

	def ruleTwo(self, variables, changed):
		"""Rule two for constraint propagation: assign to any cell a value x 
		if x is not in the domain of any other cell in that row, column, or box."""
		for square in variables:
			candidates = variables[square]
			if len(candidates) < 2:
				break
			for value in candidates:
				found = False
				for neighbor in self.neighbors[square]:
					if value in variables[neighbor]:
						found = True
						break
				if found is False:
					if value not in variables[square]:
						assert(False)
					variables[square] = value
					self.numRuleTwo += 1
					changed = True
					break
		return [variables, changed]

	def nakedK(self, k, variables, changed):
		"""Performs the "naked triples" strategy for constraint propagation for a general k."""
		# TODO
		return [variables, changed]

	def backtrackSearch(self, variables):
		"""Perform backtracking search by trying assignments systematically. 
		Recursive function returns completed board upon success or False (backtracking) 
		upon reaching a contradiction. Based on textbook."""
		# if assignment is complete
		if self.isSolved(variables):
			return variables

		# select a variable to make assignment
		square = self.selectUnassignedVariable(variables)
		for value in self.orderDomainValues(square, variables):
			# make an assignment and perform constraint propagation
			newVariables = variables.copy()
			newVariables[square] = value
			newVariables = self.constraintPropagation(newVariables)

			# keep searching until no candidates left for some cell or entire board is solved
			if newVariables is not False:
				result = self.backtrackSearch(newVariables)
				if result is not False:
					return result
		# backtrack
		self.numBacktrackings += 1
		return False

	def selectUnassignedVariable(self, variables):
		"""Select an unassigned variable (square) to try an assignment. 
		Helper method to switch among different heuristics."""
		if self.useRandomUnassignedVariable is True:
			return self.selectRandomVariable(variables)
		else:	
			return self.selectMostConstrainedVariable(variables)

	def selectMostConstrainedVariable(self, variables):
		"""Select the least constraining unassigned variable to try an assignment."""
		minLength = 10
		minSquare = ""
		for square in variables:
			length = len(variables[square])
			if length < minLength and length > 1:
				minSquare = square
				minLength = length
		return minSquare

	def selectRandomVariable(self, variables):
		"""Select a random unassigned variable to try an assignment."""
		squaresRemaining = [square for square in variables if len(variables[square]) > 1]
		return choice(squaresRemaining)

	def orderDomainValues(self, var, variables):
		"""Order the domain values."""
		return variables[var]
