#!/usr/bin/env python
from Agent import *
import random
import numpy
import pylab

class Environment:
	"""The Environment class manages the vacuum world and agent position/orientation."""

	# world is composed of nxm cells with probability p of dirt
	world = None
	n = 0
	m = 0
	p = 0

	# home cell,  initialized in __init__
	HOME_X = 0
	HOME_Y = 0

	# number of clean cells
	num_clean_cells = 0

	# agent has (x, y) coordinates and 4 possible facing directions
	agent_x = 0
	agent_y = 0
	agent_facing = 0

	def __init__(self, n, m, p):
		self.n = n
		self.m = m
		self.p = p

		self.HOME_X = 0 # leftmost,
		self.HOME_Y = m-1 # bottom corner

		self.num_clean_cells = n*m

		# 0 = clean, 1 = dirt
		self.world = [0]*n*m
		for row in range(0, m):
			for col in range(0, n):
				if random.random() < p:
					self.world[row*n+col] = 1
					self.num_clean_cells -= 1

		self.agent_x = self.HOME_X
		self.agent_y = self.HOME_Y
		self.agent_facing = Agent.NORTH # 0 = N, 1 = E, 2 = S, 3 = W

	def getPercept(self):
		wall = self.__isWallAhead__()
		dirt = self.world[self.agent_y*self.n+self.agent_x]
		home = 1 if self.agent_x == self.HOME_X and self.agent_y == self.HOME_Y else 0
		return [wall, dirt, home]

	def __isWallAhead__(self):
		temp_x = self.agent_x
		temp_y = self.agent_y
		if self.agent_facing == Agent.NORTH:
			temp_y -= 1
		if self.agent_facing == Agent.EAST:
			temp_x += 1
		if self.agent_facing == Agent.SOUTH:
			temp_y += 1
		if self.agent_facing == Agent.WEST:
			temp_x -= 1

		if temp_x < 0 or temp_y < 0 or temp_x >= self.n or temp_y >= self.m:
			return 1
		else:
			return 0

	def updateWorld(self, action):
		if action == Agent.FORWARD and self.__isWallAhead__() != 1:
			if self.agent_facing == Agent.NORTH:
				self.agent_y -= 1
			if self.agent_facing == Agent.EAST:
				self.agent_x += 1
			if self.agent_facing == Agent.SOUTH:
				self.agent_y += 1
			if self.agent_facing == Agent.WEST:
				self.agent_x -= 1
		if action == Agent.RIGHT:
			self.agent_facing = (self.agent_facing + 1) % 4
		if action == Agent.LEFT:
			self.agent_facing = (self.agent_facing - 1) % 4
		if action == Agent.SUCK:
			if self.world[self.agent_y*self.n+self.agent_x] != 0:
				self.world[self.agent_y*self.n+self.agent_x] = 0
				self.num_clean_cells += 1
		if action == Agent.OFF:
			return False
		else:
			return True

	def getNumCleanCells(self):
		return self.num_clean_cells

	def printCurrentWorld(self):
		w = self.world
		m = self.m
		n = self.n
		x = self.agent_x
		y = self.agent_y
		f = self.agent_facing

		for row in range(0, m):
			print "+--"*n + "+"

			string = ""
			for col in range(0, n):
				if w[row*n+col] == 1:
					string += "|."
				else:
					string += "| "
				if row == y and col == x:
					if f == Agent.NORTH:
						string += "N"
					if f == Agent.EAST:
						string += "E"
					if f == Agent.SOUTH:
						string += "S"
					if f == Agent.WEST:
						string += "W"
				else:
					string += " "
			print string + "|"

		print "+--"*n + "+"
		print

    	def performance(self,num_clean_cells, draw):
            	print "Mean performance comparing to ideal case: %f" % numpy.mean([x*1.0 / y for x,y in zip(num_clean_cells, range(1,len(num_clean_cells)+1))])
        	if draw == 1:
            		pylab.plot(range(1,len(num_clean_cells)+1), num_clean_cells)
                    	pylab.xlabel('number of actions')
                    	pylab.ylabel('number of clean cells')
                    	pylab.title('performance curve')
                    	pylab.grid(True)
            		pylab.show()

