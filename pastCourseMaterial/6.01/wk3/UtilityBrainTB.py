import math

### Actions

# A conservative speed factor
speed = 0.5

# An action is a list: the first element is a name string, the second is a
# list of arguments for motorOutput.

# Some basic robot actions

stop = ["stop", [0,0]]
go = ["go", [speed,0]]
left = ["left", [0,speed]]
right = ["right", [0,-speed]]

# Selecting out the parts of the action: the args for motorOutput and a string
# that describes the action (for debugging)

def actionArgs(action):
   return action[1]

def actionString(action):
   return action[0]

# List of all available actions
# Note that this is a list of procedures
allActions = [stop, go, left, right]

######################################################################
#
#    Behaviors
# 
######################################################################


### A behavior is represented as a procedure (a utility
### function), that that takes an action as input and returns a number
### that indicates how much that behavior "prefers" that action.

# Primitive wandering behavior
def wander(poseValues, rangeValues):
   def uf(action): 
      if action == stop: return 0
      elif action == go: return 10
      elif action == left: return 2
      elif action == right: return 2
      else: return 0
   return uf

# Primitive behavior for avoiding obstacles
# rangeValues is a list of the distances reported by the sonars
def avoid(poseValues, rangeValues):

   # Parameters for clip
   mindist = 0.2
   maxdist = 1.2

   # clip a given value between mindist and maxdist and scale from 0 to 1
   def clip(value, mindist, maxdist):
      return (max(mindist, min(value, maxdist)) - mindist)/(maxdist - mindist)

   # Stopping is not that useful.
   stopU = 0

   # Going forward away from obstacles, is useful when there are nearby
   # obstacles.  The utility of going forward is greater with greater free space
   # in front of the robot.  To compute the utility we read the front sonars and
   # find the minimum distance to a perceived object.  We clip shortest observed
   # distance, and scale the result between 0 and 10

   minAnyDist = min(rangeValues)
   minFrontDist =  min(rangeValues[2:6])
   if minAnyDist <= maxdist/3:
      goU = clip(minFrontDist, mindist, maxdist) * 10
   else:
      goU = 0

   # For turning, it's always good to turn, but bias the turn in favor of
   # the free direction.  In fact, the robot can sometimes get stuck when it
   # tries to turn in place, because it isn't circular and the back
   # hits an obstacle as it swings around.  Think about ways to fix
   # this bug.

   minLeftDist = min(rangeValues[0:3])
   minRightDist = min(rangeValues[5:8])
   closerToLeft = minLeftDist < minRightDist
   if closerToLeft:
      rightU = 10 - clip(minLeftDist,mindist, maxdist/3) * 10
      leftU = 0
   else:
      leftU = 10 - clip(minRightDist, mindist, maxdist/3) * 10
      rightU = 0

   # Construct the utility function and return it
   def uf(action): 
      if action == stop: return stopU
      elif action == go: return goU
      elif action == left: return leftU
      elif action == right: return rightU
      else: return 0
   return uf

# Move toward a goal position and stop

# Tolerances for positioning
tolXY = 0.1
tolAngle = math.pi/10

def seek(target, poseValues, rangeValues):

   stopU = goU = leftU = rightU = 0
   reachedXY = False
   angle = poseValues[2]
   
   if atTargetXY(poseValues, target):
      reachedXY = True
      desAngle = target[2]
      print "actual angle =", angle, "desired align angle =", desAngle
   else:
      dx =  poseValues[0] - target[0]      # proportional to cosine
      dy =  poseValues[1] - target[1]      # proportional to sine
      desAngle = math.atan2(dy, dx)+math.pi
      print "actual angle =", angle, "desired seek angle =", desAngle

   if leftOfTargetAngle(angle, desAngle):
      rightU = 5
   elif rightOfTargetAngle(angle, desAngle):
      leftU = 5
   elif reachedXY:
      stopU = 20                        # really stop
   else:
      goU = 5
      leftU = rightU = 0

   # Construct the utility function and return it
   def uf(action): 
      if action == stop: return stopU
      elif action == go: return goU
      elif action == left: return leftU
      elif action == right: return rightU
      else: return 0
   return uf

# Helper functions for seek behavior

def poseXYDist(p1,p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx**2 + dy**2)

def angleDiff(a1, a2):
   da = (a1 - a2)%(2*math.pi)
   if (da > math.pi):
      return da - 2*math.pi
   else:
      return da

def atTargetXY (poseValues, targetPoseValues):
   return poseXYDist(poseValues, targetPoseValues) < tolXY

def leftOfTargetAngle (a1, a2):
   diff = angleDiff(a1, a2)
   return diff > tolAngle 

def rightOfTargetAngle (a1, a2):
   diff = angleDiff(a1, a2)
   return diff < -tolAngle

######################################################################
#
#    Combining utility functions
# 
######################################################################

# addUf takes two utility functions and returns a new utility
# function, whose value any action is the sum of the two utilities

def addUf(u1, u2):
   print "u1:", [(actionString(a), u1(a)) for a in allActions]
   print "u2:", [(actionString(a), u2(a)) for a in allActions]
   return lambda action: u1(action) + u2(action)

# scaleUf takes a utility function and a number and returns a utility
# function whose value any action is the original utility, multiplied
# by the number

# Uncomment the next line and complete
# def scaleUf(u, scale):

######################################################################
#
#    Action selection
# 
######################################################################

## Here are two subprocedures called in the basic step.  We've isolated them
## as subprocedures to make the code more readable.

# Pick the best action for a utility function
def bestAction(u):
   values = [u(a) for a in allActions]
   maxValueIndex = values.index(max(values))
   return allActions[maxValueIndex]

# Do an action
def doAction(action):
   if action in allActions:
      # foo(*bar) calls foo with the arguments from the list bar
      # see Unpacking Argument Lists in the Python Tutorial
      motorOutput(*actionArgs(action))
   else:
      print "error, unknown action", actionString(action)

# to use a utility function u, pick the best action for that
# utility function and do that action
def useUf(u):
   action = bestAction(u)
   # Print the name of the selected action procedure for debugging
   print "Best Action: ", actionString(action)
   doAction(action)

######################################################################
#
#    Main brain
# 
######################################################################

# If we're debugging in the simulator, we can cheat and get the real
# pose of the robot in the simulated world.  Take this out if you're
# running on the real robot!
def cheatPose():
    return app().output.abspose.get()   

# We've put a blank setup method here, which you can add to later if you
# want to initialize anything
def setup():
   # do nothing
   pass

## Here is the basic step
def step():
   # for debugging it's best to read the sonar distances at a
   # well-defined point in the step look, rather than sprinkling
   # calls to sonarDistances() throughout the entire program
   rangeValues = sonarDistances()
   #poseValues = pose()
   poseValues = cheatPose()

   print "pose:", poseValues, "min range:", min(rangeValues)

   target = [1.0, 0.5, 0.0]

   # after you verify that the program runs, comment out the
   # u = wander(poseValues, rangeValues) line and uncomment the u=addUf(...) line
   # and see how the behavior changes
   # u = seek(target, poseValues,rangeValues)
   u = addUf(seek(target, poseValues,rangeValues), avoid(poseValues,rangeValues))
   print "Sum:", [(actionString(a), u(a)) for a in allActions]

   useUf(u)
