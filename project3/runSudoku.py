#!/usr/bin/env python
import SudokuSolver
import sys
from time import clock, time

def printUsage():
	print "Usage: " + sys.argv[0] + " [-i sequence|-f inputFile]"
	print "\tChoose one run option:"
	print "\t" + sys.argv[0] + " -i \"sequence\""
	print "\t\treads in a board sequence string"
	print "\t\te.g. \"240300000000520407000046008610700084009060500730005061100470000302051000000002019\""
	print "\t" + sys.argv[0] + " -f inputFile"
	print "\t\treads from input file"
	print "\t\tmust be formatted like repository.txt"

def validBoardSeq(seq):
	"""Checks if the board sequence is valid."""
	if len(seq) != 81:
		return False
	validSet = [str(i) for i in range(10)] 
	for i in seq:
		if i not in validSet:
			return False
	return True

### Parse command line arguments

if len(sys.argv) < 3:
	printUsage()
	exit(1)

problemSet = []
problemComments = []

if sys.argv[1] == "-i":
	if not validBoardSeq(sys.argv[2]):
		raise ValueError("Invalid board sequence.")

	problemSet.append(sys.argv[2])	
	problemComments.append("command line input")

elif sys.argv[1] == "-f":
	# open file and parse
	with open(sys.argv[2], 'r') as f:
		lines = [line.strip() for line in f]

	problem = ""
	for i, line in enumerate(lines):
		if i % 11 == 0:
			problemComments.append(line)
		elif i % 11 == 10:
			if not validBoardSeq(problem):
				raise ValueError("Invalid board sequence.")
			problemSet.append(problem)
			problem = ""
		else:
			problem += ''.join(line.split())

else:
	printUsage()
	exit(3)

### Set up sudoku solver
sudoku = SudokuSolver.SudokuSolver()
for problem, comment in zip(problemSet, problemComments):
	print "--------------------------------------------------"
	print "Running: " + comment
	
	sudoku.setup(problem)
	print "\nInitial board:"
	sudoku.printBoard()

	print "Solving...",
	startClock = time()
	(success, numBacktracking) = sudoku.solve()
	endClock = time()

	print "done."
	print "\nFinal board:"
	sudoku.printBoard()

	print "Time: ", endClock - startClock
