#!/usr/bin/env python
from Agent import *
import numpy

class RandomizedAgent(Agent):
    def __init__(self):
        self.multinomials = dict([((1,0,1), [0.3,0,0,0.7,0]),
                            ((1,1,0), [0,0.1,0.1,0.8,0]),
                            ((1,1,1), [0,0.1,0.1,0.8,0.0]),
                            ((1,0,0), [0.1,0.1,0.1,0.7,0.0]),
                            ((0,0,1), [0.6,0.2,0.2,0,0.0]),
                            ((0,1,0), [0,0.5,0.5,0,0.0]),
                            ((0,1,1), [0,0.5,0.48,0,0.02]),
                            ((0,0,0), [0.4,0.3,0.3,0,0.0]),
                            ])

    def takeStep(self, percept):
        [wall, dirt, home] = percept
        action = list(numpy.random.multinomial(1,self.multinomials[(dirt,wall,home)])).index(1) + 1
        return action

