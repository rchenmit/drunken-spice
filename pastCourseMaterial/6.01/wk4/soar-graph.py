import diffeq
reload(diffeq)   # in case it's changed
from diffeq import *

g1 = GraphingWindow (400 , 400 , 0, 20, -100, 100 , " diffeq ")
f = solveDiffEq ([0 , 1], [2, -2])
g1. graphDiscrete ( lambda x: f(x), 'blue')
