import math

class TBSequence:
    def __init__(self, actions):
        self.actions = actions

    def start(self):
        self.counter = 0
        self.actions[0].start()

    # Add the step and done methods here.

class GoForwardUntilXLimit:
    def __init__(self, xLimit):
        self.xLimit = xLimit

    def start(self):
        pass
        
    def step(self):
        motorOutput(0.1, 0.0)

    def done(self):
        return pose()[0] > self.xLimit

######################################################################
#   Brain
######################################################################

def setup():
    robot.behavior = GoForwardUntilXLimit(1.0)
    robot.behavior.start()
    
def step():
    if robot.behavior.done():
        motorOutput(0.0,0.0)
    else:
        robot.behavior.step()

######################################################################
#   Helper functions
######################################################################

# You may find these handy

def poseDist((x1,y1,th1),(x2,y2,th2)):
   return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def within(a, b, eps):
    return abs(a - b) < eps

def nearAngle(a1,a2,eps):
   return abs(fixAnglePlusMinusPi(a1-a2)) < eps

# Put betwen minus pi and pi
def fixAnglePlusMinusPi(a):
   if a > math.pi:
      return fixAnglePlusMinusPi(a - 2.0* math.pi)
   elif a < -math.pi:
      return fixAnglePlusMinusPi(a + 2.0*math.pi)
   else:
      return a


    


