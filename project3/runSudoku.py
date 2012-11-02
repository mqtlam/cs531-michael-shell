#!/usr/bin/env python
import SudokuSolver
import sys
from time import clock, time

def printUsage():
	print "Usage: " + sys.argv[0] + " (-i sequence|-f inputFile) [--random|--naked K]"
	print "\n\tChoose one run option:"
	print "\t" + sys.argv[0] + " -i \"sequence\""
	print "\t\treads in a board sequence string"
	print "\t\te.g. \"240300000000520407000046008610700084009060500730005061100470000302051000000002019\""
	print "\t" + sys.argv[0] + " -f inputFile"
	print "\t\treads from input file"
	print "\t\tmust be formatted like repository.txt"
	print "\n\tOptional Arguments (must be specified after run option above):"
	print "\t\t--random: picks random slot instead of most constrained slot for unassigned variable heuristic"
	print "\t\t--naked K: enables naked-K rule, where K is a string of integers 1-9,"
	print "\t\t\te.g. --naked 23 enables naked doubles (K=2) and naked triples rules (K=3)."

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

# Optional Arguments
useRandomUnassignedVariable = False
useNakedStrategy = []

if len(sys.argv) > 3:
	i = 3
	while i < len(sys.argv):
		if sys.argv[i] == "--random":
			useRandomUnassignedVariable = True
		if sys.argv[i] == "--naked":
			if i+1 < len(sys.argv):
				useNakedStrategy = [int(x) for x in set(sys.argv[i+1])]
				print useNakedStrategy
			else:
				printUsage()
				exit(4)
		i+=1

### Set up sudoku solver
sudoku = SudokuSolver.SudokuSolver(useRandomUnassignedVariable, useNakedStrategy)
for problem, comment in zip(problemSet, problemComments):
	print "--------------------------------------------------"
	print "Running: " + comment
	
	sudoku.setup(problem)
	print "\nInitial board:"
	sudoku.printBoard()

	print "Solving...",
	(success, numBacktracking, numRuleOne, numRuleTwo, numNakedStrategy, numFilledIn, time) = sudoku.solve()

	print "success." if success else "failed."
	print "\nFinal board:"
	sudoku.printFullBoard()

	print "Time: \t\t\t\t", time
	print "Initially filled: \t\t", numFilledIn
	print "Num backtrackings: \t\t", numBacktracking
	print "Num Rule One's: \t\t", numRuleOne
	print "Num Rule Two's: \t\t", numRuleTwo
	for k in numNakedStrategy:
		print "Num Rule Three's ( K =", k, "):\t", numNakedStrategy[k]
