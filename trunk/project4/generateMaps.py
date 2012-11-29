#! /usr/bin/python

"""
Randomly generates maps of the wumpus world
"""

import random
import os.path

def randomSquare(size):
	"""
	Randomly picks a square
	"""
	x = 0
	y = 0

	#the starting square is not a valid choice
	while x == 0 and y ==0:
		x = random.randint(0,size-1)
		y = random.randint(0,size-1)

	return (x,y)

class Puzzle(object):
	"""
	Represents a map randomly generated according to the wampus rules.
	size the magnitude of the one of the dimensions
	"""

	def __init__(self, size):
		"""
		Inits the new puzzle
		"""
		self.size = size
		self.solveable = False
		self.gold = None
		self.pits = list()
		self.wumpus = None

	def generate(self):
		"""
		randomly generates itself
		"""
		#create all the pits
		for i in range(self.size):
			for j in range(self.size):

				#roll for a pit
				if random.random() <= .2 and not (i == 0 and j == 0) :
					puzzle.addPit(i,j)

		#pick a square for the wumpus
		self.addWumpus( *randomSquare(self.size) )

		#pick a square for the gold
		self.addGold( *randomSquare(self.size) )

	def writeToFile(self, fileName):
		"""
		Writes the puzzle to a file
		"""
		outFile = open(fileName, "w")

		#write out the wumpus
		outFile.write("w: %i,%i\n" % self.wumpus)

		#write out the gold
		outFile.write("g: %i,%i\n" % self.gold)

		#write out the pits
		for coord in self.pits:
			outFile.write("p: %i,%i\n" % coord)

	def addGold(self, x, y):
		"""
		Sets the location of the gold
		"""
		self.gold = (x,y)

	def addPit(self, x, y):
		"""
		Adds a pit to the board
		"""
		self.pits.append( (x,y) )

	def addWumpus(self, x, y):
		"""
		Adds a wumpus to the board
		"""
		self.wumpus = (x,y)

#main!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#sizes = [10, 25, 50, 100]
sizes = [4]
quantityPer = 40
basePath = "./maps/"

#generate all the puzzles
for size in sizes:

	for i in range(quantityPer):
		puzzle = Puzzle(size)
		puzzle.generate()
		puzzle.writeToFile(os.path.join(basePath, "%i_%i" % (size,i)))


