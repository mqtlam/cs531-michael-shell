#!/usr/bin/env python
from MemorylessAgent import *
from RandomizedAgent import *
from ModelBasedAgent import *

import sys
import random

## Process command line arguments

def printUsage():
	print 'Usage: ' + sys.argv[0] + ' 1|2|3 [n m p]'
	print '\t1 = memoryless, 2 = randomized, 3 = model-based'
	print '\tn by m grid with p probability (0.0-1.0)'

if len(sys.argv) < 2:
	printUsage()
	sys.exit(1)

agent_type = int(sys.argv[1])
agent = None
if agent_type == 1:
	agent = MemorylessAgent()
elif agent_type == 2:
	agent = RandomizedAgent()
elif agent_type == 3:
	agent = ModelBasedAgent()
else:
	printUsage()
	sys.exit(2)

n = int(sys.argv[2]) if len(sys.argv) > 2 else 10 # columns
m = int(sys.argv[3]) if len(sys.argv) > 3 else 10 # rows
p = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0 # probability of dirt

if n <= 0 or m <= 0:
	printUsage()
	sys.exit(3)

if p < 0.0 or p > 1.0:
	printUsage()
	sys.exit(4)

## Set up environment

num_actions = 0
num_clean_cells = n*m

# 0 = clean, 1 = dirt
environment = [0]*n*m
for row in range(0,m):
	for col in range(0,n):
		if random.random() < p:
			environment[row*n+col] = 1
			num_clean_cells -= 1

## Set up agent orientation and position
agent_x = 0 # leftmost,
agent_y = m-1 # bottom corner 
agent_facing = Agent.NORTH # 0 = N, 1 = E, 2 = S, 3 = W 

## Main loop
running = True
while (running):
	# set up percepts
	temp_x = agent_x
	temp_y = agent_y
	if agent_facing == Agent.NORTH:
		temp_y -= 1
	if agent_facing == Agent.EAST:
		temp_x += 1
	if agent_facing == Agent.SOUTH:
		temp_y += 1
	if agent_facing == Agent.WEST:
		temp_x -= 1

	wall = 1 if temp_x < 0 or temp_y < 0 or temp_x >= n or temp_y >= m else 0 
	dirt = environment[agent_x*n+agent_y]
	home = 1 if agent_x == 0 and agent_y == m-1 else 0

	# agent performs a step
	action = agent.takeStep([wall, dirt, home])

	# update environment and counters 
	if action == Agent.FORWARD and wall != 1:
		if agent_facing == Agent.NORTH:
			agent_y -= 1
		if agent_facing == Agent.EAST:
			agent_x += 1
		if agent_facing == Agent.SOUTH:
			agent_y += 1
		if agent_facing == Agent.WEST:
			agent_x -= 1
	if action == Agent.RIGHT:
		agent_facing = (agent_facing + 1) % 4
	if action == Agent.LEFT:
		agent_facing = (agent_facing - 1) % 4
	if action == Agent.SUCK:
		if environment[agent_x*n+agent_y] != 0:
			environment[agent_x*n+agent_y] = 0	
			num_clean_cells += 1
	if action == Agent.OFF:
		running = False
	num_actions += 1

print "Number of actions: " + str(num_actions)
print "Number of clean cells: " + str(num_clean_cells) + "/" + str(n*m)
