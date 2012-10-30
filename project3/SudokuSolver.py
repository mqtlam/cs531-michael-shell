#!/usr/bin/env python
from time import clock, time

class SudokuSolver:
	"""The Sudoku class represents a sudoku board."""

	def __init__(self):
		"""Initialize the Sudoku board and CSP formulation."""

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
		self.numBacktracking = 0
		self.solved = None

	def setup(self, board):
		"""Initializes the board configuration to board."""
		# reset all variables
		self.__init__()

		# set up board
		for i, digit in enumerate(board):
			index = '' + self.rows[i/9] + self.cols[i%9]
			if digit != "0":
				self.variables[index] = digit

	def solve(self):
		"""Attempts to solve the current board."""
		if self.solved is not None:
			return self.solved

		startClock = time()
		self.constraintPropagation()
		endClock = time()

		# [success?, numBacktracking, time to solve] # TODO: return more statistics
		self.solved = [self.isSolved(), 0, endClock - startClock]
		return self.solved 

	def isSolved(self):
		"""Returns true if the current board is solved."""
		for square in self.neighbors:
			if len(self.variables[square]) != 1:
				return False
			for neighbor in self.neighbors[square]:
				if len(self.variables[neighbor]) != 1:
					return False
				elif self.variables[neighbor] == self.variables[square]:
					return False
		return True

	def printBoard(self):
		"""Prints the current board. For debugging purposes."""
		print "  a b c   d e f   g h i"
		for r in self.rows:
			print r, ''.join((self.variables[r+c] if len(self.variables[r+c]) == 1 else '-')+' '+('| ' if c in 'cf' else '') for c in self.cols)
			if r in '36':
				print ' ' + '-'*23
		print

	def printFullBoard(self):
		"""Prints the current board, complete with the domain for each variable. For debugging purposes."""
		width = 1+max(len(self.variables[s]) for s in self.squares)
		print '  ' + ''.join(c.center(width)+('  ' if c in 'cf' else '') for c in "abcdefghi")
		for r in self.rows:
			print r, ''.join(self.variables[r+c].center(width)+('| ' if c in 'cf' else '') for c in self.cols)
			if r in '36':
				print ' -' + '-'.join(['-'*(width*3)]*3)
		print

	### CSP Functions

	def constraintPropagation(self):
		changed = True
		while changed:
			changed = False
			for square in self.variables:
				value = self.variables[square]
				if len(value) == 1:
					for neighbor in self.neighbors[square]:
						if value in self.variables[neighbor]:
							self.variables[neighbor] = self.variables[neighbor].replace(value,'')
							changed = True
	
	# TODO
	def search(self):
		pass
