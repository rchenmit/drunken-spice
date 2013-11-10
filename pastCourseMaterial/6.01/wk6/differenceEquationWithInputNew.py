import math
import polynomial
from polynomial import *
from time import time

# Timef takes a function and returns a function.  The returned function can
# be called with n and returns the time required to compute f(n)
def timef(f):
    def timefn(n):
        t1 = time()
        f(n)
        t2 = time()
        return(t2 - t1)
    return timefn

######################################################################
###                 DifferenceEquationWithInput
######################################################################

# Linear difference equations of any order, with input
# Note that the inputSource is part of the definition

class DifferenceEquationWithInput:
    # Solves yCoeffs[0]*y(n+K) + .. + yCoeffs[K]*y(n) =
    #                 xCoeffs[0]*x(n+L) + + xCoeffs[L]*x(n)
    # initVals are [y(K-1),..,y(0)]
    # x is a function which takes an positive integer argument
    def __init__(self, initVals, yCoeffs, xCoeffs, x):
        print ("inits", initVals, "yCoeffs", yCoeffs, "xCoeffs", xCoeffs)
        assertSameLength(initVals, yCoeffs[1:])
        self.initialValues = floatList(initVals)
        self.outCoefficients = floatList(yCoeffs)
        self.inputCoefficients = floatList(xCoeffs)
        self.yOrder = len(self.initialValues)
        self.inputOrder = len(self.inputCoefficients)
        self.inputSource = x
        # Put the initial conditions in stored values.
        self.storedValues = {}
        for i in range(self.yOrder):
            self.storedValues[self.yOrder-i-1] = self.initialValues[i]
        # Test if there are trailing zeros in y and warn
        if self.outCoefficients[-1] == 0:
            print "Warning, the coefficient of y(0) = 0."
            print "Consider shifting the equation to avoid unexpected results."

    # Uses inputOrder values starting from yOrder points back from n
    def evalInput(self,n):
        K = self.yOrder
        L = self.inputOrder
        Xs = dotProd(self.inputCoefficients,
                     map(self.inputSource,
                         range(n + L - K -1, n - K -1, -1)))
        return Xs
    
    # n is the index for the value        
    def valRecur(self, n):
        if n in self.storedValues:
            return self.storedValues[n]
        else:
            K = self.yOrder
            oldYs = dotProd(self.outCoefficients[1:],
                            [self.valRecur(n-i-1) for i in range(K)])
            Xs = self.evalInput(n)
            return (Xs - oldYs)/self.outCoefficients[0]

    def valIter(self, ni):
        if ni in self.storedValues:
            return self.storedValues[ni]
        else:
            n = self.yOrder
            vals = [self.storedValues[n-i-1] for i in range(n)]
            while n <= ni:
                oldYs = dotProd(self.outCoefficients[1:],vals)
                Xs = self.evalInput(n)
                nextVal = (Xs - oldYs)/self.outCoefficients[0]
                vals = [nextVal] + vals[:-1]
                n += 1
            return vals[0]

    def __str__( self ):
        cof = self.outCoefficients
        order = len(cof)
        print " + ".join([diffEqStrh(cof[i], order-i-1, "y") for i in range(order)])
        print "="
        cof = self.inputCoefficients
        order = len(cof)
        print " + ".join([diffEqStrh(cof[i], order-i-1, "x") for i in range(order)])
        return("")

    # return the transfer function associated with this difference
    # equation 
    def z(self):
        return TransferFunction(self.inputCoefficients,
                                self.outCoefficients)

######################################################################
###                 Transfer functions
######################################################################

# This needs the following methods:
# __init__ - to create an instance
# __str__ - to construct a string to represent the transfer function
# compose - to compose two transfer functions 
# feedback - to apply Black's formula
# naturalFreqs - to get the natural frequencies
# diffEq - to return an instance of the DifferenceEquationWithInput class

# class TransferFunction:
## Fill this in

######################################################################
###                 Helper functions, not part of any class
######################################################################

# Nice printing utility
def diffEqStrh( coef, power, symb ):
    if ( power == 0 ):
        return "%.2f*%s[n]" % (coef, symb)
    return "%.2f*%s[n+%d]" % (coef, symb,power)

# Converts a list in to type float
def floatList(a):
    return [float(a[i]) for i in range(len(a))]

# a and b are lists of numbers, same length
# return sum(a[1]*b[1], ..., a[n]*b[n])
def dotProd(a, b):
    assertSameLength(a,b)
    return sum(vectorMult(a,b))

# a and b are lists of numbers, same length
# return (a[1]*b[1], ..., a[n]*b[n])
def vectorMult(a, b):
    assertSameLength(a,b)
    return [ai*bi for (ai,bi) in zip(a,b)]
        
######################################################################
###                 Transfer function utilities
######################################################################

## This is an example of an inputSource
def unitSample(n):
    if n == 0:
        return 1
    else:
        return 0

def unitSamplep5(n):
    if n == 5:
        return 1
    else:
        return 0

def unitSamplep6(n):
    if n == 6:
        return 1
    else:
        return 0

