#from MemorylessAgent import *
#from RandomizedAgent import *
#from ModelBasedAgent import *
from Environment import *
from Agent import *

import numpy
import pylab

#class FakeMemorylessAgent(Agent):
#    actions = [0] * 8
#	def __init__(self, a):
#		self.actions = a
#
#	def takeStep(self, percept):
#		[wall, dirt, home] = percept
#        if dirt == 1 and wall == 0 and home == 1:
#            return self.actions[0]
#        if dirt == 1 and wall == 1 and home == 0:
#            return self.actions[1]
#        if dirt == 1 and wall == 1 and home == 1:
#            return self.actions[2]
#        if dirt == 1 and wall == 0 and home == 0:
#            return self.actions[3]
#        if dirt == 0 and wall == 0 and home == 1:
#            return self.actions[4]
#        if dirt == 0 and wall == 1 and home == 0:
#            return self.actions[5]
#        if dirt == 0 and wall == 1 and home == 1:
#            return self.actions[6]
#        if dirt == 0 and wall == 0 and home == 0:
#            return self.actions[7]
#		# implement
#        #return Agent.OFF

class FakeMemorylessAgent(Agent):
    actions = [0] * 8
    def __init__(self,a):
        self.actions = a

    def takeStep(self, percept):
        [wall, dirt, home] = percept
        if dirt == 1 and wall == 0 and home == 1:
            return self.actions[0]
        if dirt == 1 and wall == 1 and home == 0:
            return self.actions[1]
        if dirt == 1 and wall == 1 and home == 1:
            return self.actions[2]
        if dirt == 1 and wall == 0 and home == 0:
            return self.actions[3]

        if dirt == 0 and wall == 0 and home == 1:
            return self.actions[4]
        if dirt == 0 and wall == 1 and home == 0:
            return self.actions[5]
        if dirt == 0 and wall == 1 and home == 1: # this is not possible
            return self.actions[6]
        if dirt == 0 and wall == 0 and home == 0:
            return self.actions[7]

def performance(num_clean_cells, draw):
    print numpy.mean([x*1.0 / y for x,y in zip(num_clean_cells, range(1,len(num_clean_cells)+1))])
    if draw == 1:
        pylab.plot(range(1,len(num_clean_cells)+1), num_clean_cells)
        pylab.show()

def brute_force(max_steps):
    best_action_num = 0
    best_clean_cells = 0

    actions = [1, 4, 4, 1, 2, 2, 2, 2]

    agent = FakeMemorylessAgent(actions)

    n = 4
    m = 4
    p = 1.0

    ## Set up world environment
    environment = Environment(n, m, p)

    ## Main loop
    MAX_ACTIONS = max_steps # prevent from running forever
    num_actions = 0
    num_clean_cells = [0] * max_steps
    running = True
    while (running and num_actions < MAX_ACTIONS):
        # print current world
        print "Action " + str(num_actions)
        environment.printCurrentWorld()

        # set up percept
        percept = environment.getPercept()

        # agent performs a step
        action = agent.takeStep(percept)

        # update environment and counters
        running = environment.updateWorld(action)

        # print num actions & num clean cells
        num_clean_cells[num_actions] = environment.getNumCleanCells()
        num_actions += 1
        print str(num_actions) + ", " + str(num_clean_cells)

    return num_clean_cells
