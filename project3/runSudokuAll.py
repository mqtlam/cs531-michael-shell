#!/usr/bin/env python
import SudokuSolver
import sys
from time import clock, time

def printUsage():
	print "Usage: " + sys.argv[0] + " (-i sequence|-f inputFile) [--nosearch|--random|--ruletwo|--naked K]"
	print "\t** By default, runs backtracking search with contraint propagation and only rule one."
	print "\t   Add optional arguments to add on rules."
	print "\n\tChoose one run option:"
	print "\t" + sys.argv[0] + " -i \"sequence\""
	print "\t\treads in a board sequence string"
	print "\t\te.g. \"240300000000520407000046008610700084009060500730005061100470000302051000000002019\""
	print "\t" + sys.argv[0] + " -f inputFile"
	print "\t\treads from input file"
	print "\t\tmust be formatted like repository.txt"
	print "\n\tOptional Arguments (must be specified after run option above):"
	print "\t\t--nosearch: disables backtracking search, only using constraint propagation and rules until convergence"
	print "\t\t--random: picks random slot instead of most constrained slot for unassigned variable heuristic"
	print "\t\t--ruletwo: enables rule two, which assigns to any cell a value x if x is not in the domain of any other cell in that unit"
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
noSearch = False
useRandomUnassignedVariable = False
useRuleTwo = False
useNakedStrategy = []

if len(sys.argv) > 3:
	i = 3
	while i < len(sys.argv):
		if sys.argv[i] == "--nosearch":
			noSearch = True
		if sys.argv[i] == "--random":
			useRandomUnassignedVariable = True
		if sys.argv[i] == "--ruletwo":
			useRuleTwo = True
		if sys.argv[i] == "--naked":
			if i+1 < len(sys.argv):
				useNakedStrategy = [int(x) for x in set(sys.argv[i+1])]
			else:
				printUsage()
				exit(4)
		i+=1

#---------------------------------------------------------------------------

nBacktracks = []
nRuleOnes = []
nRuleTwos = []
nRuleNakedK = [[],[]]

easy = []
med = []
hard = []
evil = []

IsSucc = []

nFilledIn = []

import re

#---------------------------------------------------------------------------

### Set up sudoku solver
sudoku = SudokuSolver.SudokuSolver(noSearch, useRandomUnassignedVariable, useRuleTwo, useNakedStrategy)
for problem, comment in zip(problemSet, problemComments):
	print "--------------------------------------------------"
	print "Running: " + comment

    	fstr = re.search('[a-zA-Z][a-zA-Z]', comment)
    	fstr = fstr.group(0)

    	if fstr == 'ea' or fstr == 'Ea':
        	easy.append(1.0)
        	med.append(0.0)
        	hard.append(0.0)
        	evil.append(0.0)
        elif fstr == 'me' or fstr == 'Me':
        	easy.append(0.0)
        	med.append(1.0)
        	hard.append(0.0)
        	evil.append(0.0)
    	elif fstr == 'ha' or fstr == 'Ha':
        	easy.append(0.0)
        	med.append(0.0)
        	hard.append(1.0)
        	evil.append(0.0)
    	elif fstr == 'ev' or fstr == 'Ev':
        	easy.append(0.0)
        	med.append(0.0)
        	hard.append(0.0)
        	evil.append(1.0)
    	else:
            	print fstr
        	easy.append(0.0)
        	med.append(0.0)
        	hard.append(0.0)
        	evil.append(0.0)

	sudoku.setup(problem)
	print "\nInitial board:"
	sudoku.printBoard()

	print "Solving...",
	(success, numBacktracking, numRuleOne, numRuleTwo, numNakedStrategy, numFilledIn, time) = sudoku.solve()

    	IsSucc.append(int(success))

	print "success." if success else "failed."
	print "\nFinal board:"
	sudoku.printFullBoard()

	print "Time: \t\t\t\t", time
	print "Initially filled: \t\t", numFilledIn
	print "Num backtrackings: \t\t", numBacktracking
	print "Num Rule One's: \t\t", numRuleOne
	if useRuleTwo is True:
		print "Num Rule Two's: \t\t", numRuleTwo
	for i,k in enumerate(numNakedStrategy):
		print "Num Rule Three's ( K =", k, "):\t", numNakedStrategy[k]
        	nRuleNakedK[i].append(numNakedStrategy[k])

    	nBacktracks.append(numBacktracking)
    	nRuleOnes.append(numRuleOne)
    	nRuleTwos.append(numRuleTwo)
    	nFilledIn.append(numFilledIn)

#---------------------------------------------------------------------------

from numpy import *
easy = array(easy)
med = array(med)
hard = array(hard)
evil = array(evil)
IsSucc = array(IsSucc)

fill = array(nFilledIn)
r1 = array(nRuleOnes)
r2 = array(nRuleTwos)
n2 = array(nRuleNakedK[0])
n3 = array(nRuleNakedK[1])
bt = array(nBacktracks)

print "easy solved: %d / %d" % (dot(easy,IsSucc), sum(easy))
print "med solved: %d / %d" % (dot(med,IsSucc), sum(med))
print "hard solved: %d / %d" % (dot(hard,IsSucc), sum(hard))
print "evil solved: %d / %d" % (dot(evil,IsSucc), sum(evil))

print "Average filled-in num: easy:%f, med:%f, hard:%f, evil:%f" % (dot(fill,easy)/sum(easy), dot(fill,med)/sum(med), dot(fill,hard)/sum(hard), dot(fill,evil)/sum(evil))

# to run this in the setting r1+r2+n2+n3+btSearch
print "Average r1 num: easy:%f, med:%f, hard:%f, evil:%f" % (dot(r1,easy)/sum(easy), dot(r1,med)/sum(med), dot(r1,hard)/sum(hard), dot(r1,evil)/sum(evil))
print "Average r2 num: easy:%f, med:%f, hard:%f, evil:%f" % (dot(r2,easy)/sum(easy), dot(r2,med)/sum(med), dot(r2,hard)/sum(hard), dot(r2,evil)/sum(evil))
print "Average n2 num: easy:%f, med:%f, hard:%f, evil:%f" % (dot(n2,easy)/sum(easy), dot(n2,med)/sum(med), dot(n2,hard)/sum(hard), dot(n2,evil)/sum(evil))
print "Average n3 num: easy:%f, med:%f, hard:%f, evil:%f" % (dot(n3,easy)/sum(easy), dot(n3,med)/sum(med), dot(n3,hard)/sum(hard), dot(n3,evil)/sum(evil))
print "Average bt num: easy:%f, med:%f, hard:%f, evil:%f" % (dot(bt,easy)/sum(easy), dot(bt,med)/sum(med), dot(bt,hard)/sum(hard), dot(bt,evil)/sum(evil))

#---------------------------------------------------------------------------

### plot
plot = 0
if plot:
        import pylab
        pylab.figure(101)
        pylab.plot(range(len(nRuleOnes)), nRuleOnes, 'b.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        pylab.ylabel("number of rule one's")
        pylab.xlabel('game No.')
        #pylab.legend(loc='upper left')
        pylab.title('statistics of rule one')


        pylab.figure(102)
        pylab.plot(range(len(nRuleTwos)), nRuleTwos, 'g.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        pylab.ylabel("number of rule two's")
        pylab.xlabel('game No.')
        #pylab.legend(loc='upper left')
        pylab.title('statistics of rule two')


        for s in useNakedStrategy:
        	if s == 2:
        		pylab.figure(103)
        		pylab.plot(range(len(nRuleNakedK[0])), nRuleNakedK[0], 'r.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        		pylab.ylabel("number of naked doubles")
        		pylab.xlabel('game No.')
                #pylab.legend(loc='upper left')
        		pylab.title('statistics of naked double')

        	if s == 3:
                	if len(useNakedStrategy) > 1:
        			ns = nRuleNakedK[1]
                	else:
                    		ns = nRuleNakedK[0]
        		pylab.figure(104)
        		pylab.plot(range(len(ns)), ns, 'r.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        		pylab.ylabel("number of naked triples")
        		pylab.xlabel('game No.')
                #pylab.legend(loc='upper left')
        		pylab.title('statistics of naked triple')


        pylab.figure(105)
        pylab.plot(range(len(nBacktracks)), nBacktracks, 'y.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        pylab.ylabel("number of backtrackings")
        pylab.xlabel('game No.')
        #pylab.legend(loc='upper left')
        pylab.title('statistics of backtracking')

#-------------------------------------------------------------------------------
if 0:
        useRandomUnassignedVariable = True

        nBacktracks = []
        nRuleOnes = []
        nRuleTwos = []
        nRuleNakedK = [[],[]]

        ### Set up sudoku solver
        sudoku = SudokuSolver.SudokuSolver(noSearch, useRandomUnassignedVariable, useRuleTwo, useNakedStrategy)
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
        	if useRuleTwo is True:
        		print "Num Rule Two's: \t\t", numRuleTwo
        	for i,k in enumerate(numNakedStrategy):
        		print "Num Rule Three's ( K =", k, "):\t", numNakedStrategy[k]
                	nRuleNakedK[i].append(numNakedStrategy[k])

            	nBacktracks.append(numBacktracking)
            	nRuleOnes.append(numRuleOne)
            	nRuleTwos.append(numRuleTwo)

        ### plot
        import pylab
        pylab.figure(101)
        pylab.plot(range(len(nRuleOnes)), nRuleOnes, 'bs', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        pylab.ylabel("number of rule one's")
        pylab.xlabel('game No.')
        #pylab.legend(loc='upper left')
        pylab.title('statistics of rule one')


        pylab.figure(102)
        pylab.plot(range(len(nRuleTwos)), nRuleTwos, 'gs', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        pylab.ylabel("number of rule two's")
        pylab.xlabel('game No.')
        #pylab.legend(loc='upper left')
        pylab.title('statistics of rule two')


        for s in useNakedStrategy:
        	if s == 2:
        		pylab.figure(103)
        		pylab.plot(range(len(nRuleNakedK[0])), nRuleNakedK[0], 'rs', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        		pylab.ylabel("number of naked doubles")
        		pylab.xlabel('game No.')
                #pylab.legend(loc='upper left')
        		pylab.title('statistics of naked double')

        	if s == 3:
                	if len(useNakedStrategy) > 1:
        			ns = nRuleNakedK[1]
                	else:
                    		ns = nRuleNakedK[0]
        		pylab.figure(104)
        		pylab.plot(range(len(ns)), ns, 'rs', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        		pylab.ylabel("number of naked triples")
        		pylab.xlabel('game No.')
                #pylab.legend(loc='upper left')
        		pylab.title('statistics of naked triple')


        pylab.figure(105)
        pylab.plot(range(len(nBacktracks)), nBacktracks, 'ys', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        pylab.ylabel("number of backtrackings")
        pylab.xlabel('game No.')
        #pylab.legend(loc='upper left')
        pylab.title('statistics of backtracking')


if plot:
        pylab.show()
