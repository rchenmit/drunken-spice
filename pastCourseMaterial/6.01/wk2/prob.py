## 6.01 - Week 2 software lab

import operator

def sampleP(s):
    return s[0]
def sampleV(s):
    return s[1]

# One die

def dieSpace ():
    space = []
    for i in range(1,7):
        space.append( [1/6.0, i])
    return space

# Two dice

def diceSpace ():
    space = []
    for i in range(1,7):
        for j in range(1,7):
            space.append( [1/36.0, [i, j]] )
    return space

# The event function for sum of two dice is 5

def diceSumIs5 (sample):
    dice = sampleV(sample)
    return dice[0] + dice[1] == 5

# Definitions of events for second representation

def eventCreateI (test, space):
    return [test, space]

def eventTest(event):
    return event[0]

def eventSpace(event):
    return event[1]
