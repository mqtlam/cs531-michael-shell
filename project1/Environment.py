#!/usr/bin/env python
from Agent import *
import random

class Environment:
	"""The Environment class manages the vacuum world and agent position/orientation."""

	# world is composed of nxm cells with probability p of dirt
	world = None
	n = 0
	m = 0
	p = 0

	num_clean_cells = 0

	# agent has (x, y) coordinates and 4 possible facing directions
	agent_x = 0
	agent_y = 0
	agent_facing = 0

	def __init__(self, n, m, p):
		self.n = n
		self.m = m
		self.p = p

		self.num_clean_cells = n*m

		# 0 = clean, 1 = dirt
		self.world = [0]*n*m
		for row in range(0, m):
			for col in range(0, n):
				if random.random() < p:
					self.world[row*n+col] = 1
					self.num_clean_cells -= 1

		self.agent_x = 0 # leftmost,
		self.agent_y = m-1 # bottom corner
		self.agent_facing = Agent.NORTH # 0 = N, 1 = E, 2 = S, 3 = W
	
	def getPercept(self):
		wall = self.__isWallAhead__()
		dirt = self.world[self.agent_x*self.n+self.agent_y]
		home = 1 if self.agent_x == 0 and self.agent_y == self.m-1 else 0
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
			if agent_facing == Agent.SOUTH:
				self.agent_y += 1
			if agent_facing == Agent.WEST:
				self.agent_x -= 1
		if action == Agent.RIGHT:
			self.agent_facing = (self.agent_facing + 1) % 4
		if action == Agent.LEFT:
			self.agent_facing = (self.agent_facing - 1) % 4
		if action == Agent.SUCK:
			if self.world[self.agent_x*self.n+self.agent_y] != 0:
				self.world[self.agent_x*self.n+self.agent_y] = 0
				self.num_clean_cells += 1
		if action == Agent.OFF:
			return False

		return True

	def getNumCleanCells(self):
		return self.num_clean_cells
