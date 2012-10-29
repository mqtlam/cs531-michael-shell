#!/usr/bin/env python

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

		### Variables to keep track of statistics
		self.numSteps = 0
		self.solved = False

	def setup(self, board):
		"""Initializes the board configuration to board."""
		for i, digit in enumerate(board):
			index = '' + self.rows[i/9] + self.cols[i%9]
			# self.board[index] = digit
			if digit != "0":
				self.variables[index] = digit

		self.solved = False

	def solve(self):
		"""Attempts to solve the current board."""
		# TODO implement
		self.solved = True
		return [False, 0]

	def printBoard(self):
		"""Prints the current board."""
		print "  a b c   d e f   g h i"
		for r in self.rows:
			print r, ''.join((self.variables[r+c] if len(self.variables[r+c]) == 1 else '-')+' '+('| ' if c in 'cf' else '') for c in self.cols)
			if r in '36':
				print ' ' + '-'*23
		print

	### CSP Functions
	# TODO implement

	def ac3():
		pass

	def revise():
		pass


