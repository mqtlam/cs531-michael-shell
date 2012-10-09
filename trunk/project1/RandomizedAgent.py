#!/usr/bin/env python
from Agent import *
import numpy

class RandomizedAgent(Agent):
    def __init__(self):
        # self.multinomials = dict([((1,0,1), [0.3,0,0,0.7,0]), # (dirt, wall, home)
        #                     ((1,1,0), [0,0.1,0.1,0.8,0]),
        #                     ((1,1,1), [0,0.1,0.1,0.8,0.0]),
        #                     ((1,0,0), [0.1,0.1,0.1,0.7,0.0]),
        #                     ((0,0,1), [0.6,0.2,0.2,0,0.0]),
        #                     ((0,1,0), [0,0.5,0.5,0,0.0]),
        #                     ((0,1,1), [0,0.5,0.48,0,0.02]),
        #                     ((0,0,0), [0.4,0.3,0.3,0,0.0]),
        #                     ])
        self.multinomials = dict([((0,1,1), [0.3,0,0,0.7,0.02]), # (wall, dirt, home)
                                  ((1,1,0), [0,0.1,0.1,0.8,0.0]),
                                  ((1,1,1), [0,0.1,0.1,0.8,0.0]),
                                  ((0,1,0), [0.1,0.1,0.1,0.7,0.0]),
                                  ((0,0,1), [0.6,0.2,0.2,0,0.0]),
                                  ((1,0,0), [0,0.5,0.5,0,0.0]),
                                  ((1,0,1), [0,0.5,0.48,0,0.0]),
                                  ((0,0,0), [0.4,0.3,0.3,0,0.0]),
                            ])
        self.multinomials1 = dict([((1,0,1), [0.0,0.67,0.33,0,0.0]), # (wall, dirt, home)
                                   ((1,1,0), [0,0.0,0.0,1.0,0]),
                                   ((1,1,1), [0,0.0,0.0,1.0,0.0]),
                                   ((1,0,0), [0.0,0.67,0.33,0.0,0.0]),
                                   ((0,0,1), [0.7,0.15,0.15,0,0.0]), # at home, without wall and dirt, even stronger than (0,0,0)
                                   ((0,1,0), [0,0.0,0.0,1,0.0]),
                                   ((0,1,1), [0,0.0,0.0,1,0.0]),
                                   ((0,0,0), [0.70,0.15,0.15,0,0.0]),# should go ahead in most cases
                            ])

    def takeStep(self, percept):
        [wall, dirt, home] = percept
        action = list(numpy.random.multinomial(1,self.multinomials1[(wall,dirt,home)])).index(1) + 1
        return action

