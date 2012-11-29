import os.path

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def direction(x1, y1, x2, y2):
	"""
	Returns the direction (x2, y2) is relative to (x1, y1) or none if they
	are not in a straight line from each other
	"""
	if x1 == x2 and y2 > y1:
		return NORTH
	elif x1 == x2 and y2 < y1:
		return SOUTH
	elif y1 == y2 and x2> x1:
		return EAST
	elif y1 == y2 and x2 < x1:
		return WEST
	else:	
		return None

class Environment(object):
	"""
	Represents the environment in the wumpus world
	"""
	
	def __init__(self, fileName):
		"""
		Initializes the Environment
		fileName - the file with all the environmental data in it
		"""
		#maps coordinates to a tuple of booleans (pit, wumpus, gold), the map is
		#sparse only containing cells with objects in them
		self.map = {}
		self.size = 0
		self.readFile(fileName)
		self.fileName = fileName
		self.wumpusDead = False
	
	def canMove(self, x, y ):
		"""
		Returns true if the agent can move there, i.e. the same as the "bump" precept
		"""
		return x >= 0 and y >= 0 and x < self.size and y < self.size
	
	def shootArrow(self, x, y, direction):
		"""
		an arrow is shot from x,y in the given direction, returns true if the agent
		hears the screem
		"""
		hit = False
		
		#find the square with the wumpus
		(wx, wy) = filter( lambda c: self.map[c][1], self.map ).pop()
		
		#check the directions to see if the arrow hit the wumpus
		if direction == NORTH:
			hit = x == wx and wy > y
		
		elif direction == SOUTH:
			hit = x == wx and wy < y
		
		elif direction == EAST:
			hit = x < wx and wy == y
		
		else:
			hit = x > wx and wy == y
	
		if hit:
			self.wumpusDead = True

		return hit
		
	def sense(self, x, y):
		"""
		Returns the sense at the square a boolean tuple of (pit, wumpus, gold)
		"""
		wumpus = False
		pit = False
		gold = False
		
		#gold is only sensed on the square it is in
		if (x,y) in self.map:
			gold = self.map[(x,y)][2]
		
		#check all the neighboring squares for objects that give off precepts
		for cell in self.proxy(x,y):
			
			if cell in self.map:
				(p,w,g) = self.map[cell]
				wumpus = wumpus or w
				pit = pit or p
			
		return (pit, wumpus, gold)
	
	def isDeadly(self, x, y):
		"""
		Returns true if the given square is deadly
		"""
		deadly = False
		
		#check if there is anything interesting in the square
		if (x,y) in self.map:
			(pit,wumpus,gold) = self.map[(x,y)]
			deadly = pit or (wumpus and not self.wumpusDead)
		
		return deadly
	
	def proxy(self, x, y ):
		"""
		Returns tuples of all the squares that are proxy to the given square
		"""
		cells = [ (x+1,y), (x-1,y), (x, y+1), (x,y-1) ]
		
		return filter( lambda c: self.canMove(*c), cells )
		
	def readFile(self, fileName):
		"""
		Reads in the wumpus scienario
		"""
		#the first part of the file name is the size of the world
		self.size = int(os.path.basename(fileName).partition("_")[0])
		
		#read in each line and add its contents to the map
		for line in open(fileName, "r"):
			
			(tag, part, coord) = line.partition(": ")
			(x, delim, y) = coord.partition(",")
			
			#turn the coordinates to integers
			x = int(x)
			y = int(y)
			
			#determine what the square has
			hasWumpus = "w" in tag
			hasPit = "p" in tag
			hasGold = "g" in tag
			
			#check if the square has anything recorded for it
			if (x,y) in self.map:
				(w, p, g) = self.map[(x,y)]
				hasWumpus = hasWumpus or w
				hasPit = hasPit or p
				hasGold = hasGold or g
				
			#add the info to the square
			self.map[(x,y)] = (hasPit, hasWumpus, hasGold)
	
	def isSolveable(self):
		"""
		Returns true if the map is solveable
		"""
		# if gold is in a pit, then not solvable
		for y in range(0, self.size):
			for x in range(0, self.size):
				(pit, wumpus, gold) = (False, False, False)
				if (x,y) in self.map:
					(pit, wumpus, gold) = self.map[(x,y)]
				if (pit and gold):
					return False

		return True
		
	def noLogicalStart(self):	
		"""
		Returns true if there is no logical way to start the map
		"""
		noStart = False
		
		for cell in [(0,1), (1,0), (1,1)]:
		
			if cell in self.map:
				(pit, wumpus, gold) = self.map[cell]
				noStart = noStart or pit or wumpus
		
		return noStart
	
	def printMap(self):
		
		for y in range(self.size-1, -1, -1):
			for x in range(0, self.size):
			
				(pit,wumpus,gold) = (False, False, False)
				
				if (x,y) in self.map:
					(pit,wumpus,gold) = self.map[(x,y)]
				
				print ("%s%s%s%d%d|" % ( "p" if pit else " ", "w" if wumpus else " ", "g" if gold else " ", x, y )),
			
			print ""
			
			#print a row seperator
			print "____" * self.size
		
#test main
if __name__ == "__main__":
	e = Environment("./test_maps/4_book")
	print "should be F,F,F", e.sense(0,0)
	print "should be F,T,F", e.sense(0,1)
	print "should be T,F,F", e.sense(1,0)
	print "should be T,T,T", e.sense(1,2)
