import differenceEquationWithInput
reload(differenceEquationWithInput)   # in case it's changed
from differenceEquationWithInput import *

g1 = GraphingWindow (400 , 400 , 0, 20, 0, 1, " diffeq ")
#  insert code here
g1. graphDiscrete ( lambda x: f(x), 'blue')
