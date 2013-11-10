
##########################################################################
# Material from Lecture
##########################################################################

class PrimitiveFSM:
    def __init__(self, name, transitionfn, outputfn, initState):
        self.name = name
        self.transitionFunction = transitionfn
        self.outputFunction = outputfn
        self.state = initState

    def step(self, input):
        print self.name, " oldState: ", self.state, " input: ", input
        self.state = self.transitionFunction([self.state, input])
        output = self.outputFunction([self.state])
        print self.name, " newState: ", self.state, " output: ", output
        return output

class TableMapping:
    # Mapping with k inputs and 1 output
    # argValues is a list of lists of possible argument values
    # table is a k-1 deep nested list of lists of output values;  it
    #       has the same shape as argValues
    def __init__(self, argValues, table):
        self.argValues = argValues    
        self.table = table              
        
    def lookup(self, args):
        def recursiveLookup(args, argValues, table):
            if args[0] not in argValues[0]:
                    print "Unknown arg in lookup: ", args[0], argValues[0]
            a = argValues[0].index(args[0])
            if len(args) == 1:
                return table[a]
            else:
                return recursiveLookup(args[1:], argValues[1:], table[a])
        return recursiveLookup(args, self.argValues, self.table)

elevStates = ['opened', 'closing', 'closed', 'opening']
elevInputs = ['commandOpen', 'commandClose', 'noCommand']
transTable = [['opened', 'closing', 'opened'],
              ['opening', 'closed', 'closed'],
              ['opening', 'closed', 'closed'], 
              ['opened', 'closing', 'opened']]
outTable = ['sensorOpened', 'noSensor', 'sensorClosed', 'noSensor']
elevTrans = TableMapping([elevStates, elevInputs], transTable)
elevOut = TableMapping([elevStates], outTable)

elev = PrimitiveFSM('elevator', elevTrans.lookup, elevOut.lookup, 'closed')

##########################################################################
# For the software lab
##########################################################################

class SerialFSM:
    def __init__(self, fsm1, fsm2):
        pass

    def step(self, input):
        pass

### clockButtons
### Tell the elevator to open every 3 steps, then close

def clockTransition(args):
    [s, i] = args
    return (s + 1) % 6

def openCloseOutputs(stateArg):
    s = stateArg[0]
    if s == 0:
        return 'commandOpen'
    elif s == 3:
        return 'commandClose'
    else:
        return 'noCommand'

clockButtons = PrimitiveFSM('clockButtons', clockTransition, openCloseOutputs, 0)

##########################################################################
# For homework
##########################################################################

###########
# Feedback combination
###########

class FeedbackFSM:
    def __init__(self, fsm, initInput):
        pass
    
    def step(self, input=None):
        pass

###########
# Counter
###########

incrementer = PrimitiveFSM('incr', lambda s_i: s_i[1]+1, lambda s: s[0], 0)
counter = FeedbackFSM(incrementer, 0)

###########
# Non-Deterministic FSM
###########

class StochasticTableMapping (TableMapping):
    def lookup(self, args):
        pass

## A fully specified distribution, a probability value for every element of the
## domain, e.g. states.
class Dist:
    def __init__(self, distribution):
        self.distribution = distribution
    def __str__(self):
        return "Distribution<" + str(self.distribution) + ">"
    def draw (self):
        return multinomialDraw(self.distribution)

# Distribution is a list of pairs, the first elements of which
# numbers that sum to 1, encoding a multinomial probability
# distribution.  Generate a random draw from that distribution
def multinomialDraw(dist):
    r = random.random()
    sum = 0.0
    for i in range(len(dist)):
        sum += dist[i][0]
        if r < sum:
            return dist[i][1]

