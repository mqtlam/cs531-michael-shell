#!/usr/bin/env python
from MemorylessAgent import *
from RandomizedAgent import *
from ModelBasedAgent import *
from Environment import *

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

## Set up world environment
environment = Environment(n, m, p)

## Main loop
num_actions = 0
running = True
while (running):
	# set up percept
	percept = environment.getPercept()

	# agent performs a step
	action = agent.takeStep(percept)

	# update environment and counters 
	running = environment.updateWorld(action)
	num_actions += 1

## Results
num_clean_cells = environment.getNumCleanCells()
print "Number of actions: " + str(num_actions)
print "Number of clean cells: " + str(num_clean_cells) + "/" + str(n*m)
