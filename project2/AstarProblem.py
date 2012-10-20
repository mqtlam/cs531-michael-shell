#!/usr/bin/env python

from Heuristic import *
import copy
import sys

class State:
    """
    Represents a legal disk configuration in the Towers of Hanoi Game
    The number of pegs is hardcoded to 3: 0-2 from left to right.
    The number of disks can vary from 1 upwards. A disk is identified by an
    integer >= 1, e.g. for the 4 disk game the disks are 1, 2, 3, 4 with 4
    being the largest and 1 the smallest.
    """
    def __init__(self, copyFrom=None):
        if copyFrom:
            self.pegs = copy.deepcopy(copyFrom.pegs)
        else:
            self.pegs = [ [], [], [] ]

    def numDisksInPeg(self, pegNum):
        return len(self.pegs[pegNum])

    def addDiskToPeg(self, diskNum, pegNum):
        assert diskNum > 0
        assert pegNum >= 0 and pegNum <= 3
        #assert self.pegs and self.pegs[-1] > diskNum or not self.pegs
        self.pegs[pegNum].append(diskNum)

    def __eq__(self, other):
        for pegNum, peg in enumerate(self.pegs):
            if peg != other.pegs[pegNum]:
                return False
        return True

    def maxDiskSize(self):
        return max(max(self.pegs))

    def __hash__(self):
        "Hash function used for set container type to check quality"
        hash = 0
        shiftBy = self.maxDiskSize()
        for pegNum, peg in enumerate(self.pegs):
            subHash = 0
            for disk in peg:
                subHash += 1 << (disk - 1)
            hash += subHash << (shiftBy * pegNum)
        return hash

    def __repr__(self):
        "Disk configuration in ASCII representation"
        maxDiskSize = self.maxDiskSize()
        fullPegWidth = maxDiskSize * 2 + 1
        PEG_GAP = 2
        numpegs = len(self.pegs)
        gridWidth = fullPegWidth * numpegs + (numpegs - 1) * PEG_GAP
        numLines = maxDiskSize
        charGrid = [ [' '] * gridWidth for i in range(numLines) ]
        for peg in range(numpegs):
            pegX = peg * (fullPegWidth + PEG_GAP) + numLines
            for line in range(numLines):
                charGrid[line][pegX] = '|'
            for pos, disk in enumerate(self.pegs[peg]):
                pegY = (maxDiskSize - 1) - pos
                for x in range(pegX - disk, pegX + disk + 1):
                    if x != pegX:
                        charGrid[pegY][x] = '_'
        ret = '\n'
        for line in charGrid:
            ret += ''.join(line) + '\n'
        return ret + '\n'
    def __getitem__(self,ind):
        try:
            return self.pegs[ind]
        except IndexError:
            print 'Index of peg should be less than 2'

class AstarProblem:
    def __init__(self, initialState, goalState):
        self.initialState = copy.deepcopy(initialState)
        self.goalState = copy.deepcopy(goalState)

    def goalTest(self, state):
        return state == self.goalState

    def nextStates(self, curState):
        "Return list of all legal states that follow one step from this state"
        states = [ ]
        for pegNum, peg in enumerate(curState.pegs):
            if peg:
                diskToMove = peg[-1]
                for otherPegNum, otherPeg in enumerate(curState.pegs):
                    if (otherPeg is not peg):
                        newState = State(curState)
                        newState.pegs[pegNum].pop()
                        newState.pegs[otherPegNum].append(diskToMove)
                        states.append(newState)
        return states

