#!/usr/bin/env python
from Agent import *

class MemorylessAgent(Agent):
    def __init__(self):
        pass

    def takeStep(self, percept):
        [wall, dirt, home] = percept
        if dirt == 1 and wall == 0 and home == 1:
            return Agent.SUCK
        if dirt == 1 and wall == 1 and home == 0:
            return Agent.SUCK
        if dirt == 1 and wall == 1 and home == 1:
            return Agent.SUCK
        if dirt == 1 and wall == 0 and home == 0:
            return Agent.SUCK

        if dirt == 0 and wall == 0 and home == 1:
            return Agent.FORWARD
        if dirt == 0 and wall == 1 and home == 0:
            return Agent.RIGHT
        if dirt == 0 and wall == 1 and home == 1:
            return Agent.OFF
        if dirt == 0 and wall == 0 and home == 0:
            return Agent.FORWARD
