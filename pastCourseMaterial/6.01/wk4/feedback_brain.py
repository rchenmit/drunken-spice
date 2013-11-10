"""A SoaR 2 python brain using four distance sensors plugged to a NI-DAQ (with the NIDAQ server running) to explore
first and second order linear feedback systems."""

import numpy, math

def setup():
    read = InitNIDAQ() #We deliberately allow the exception (if there is one) to propagate.

def step():
    l,r = GetLR() # Get distances to the left and right

    angularVelocity = 0.0
    motorOutput(0.2, angularVelocity)


# The routines below support the generate 

class ServerNotRunning(Exception):
    """Raised when the NIDAQ server is not running.
    Make sure the shell command 'ps -a | grep NIDAQserver' prints something
    something. Before starting the server, be sure to unplug and replug the NIDAQ."""
    def __str__(self):
        return self.__doc__

def InitNIDAQ():
    """Return a method that can be used to pull the latest readings from the NIDAQ or throw
    a ServerNotRunning exception if NIDAQserver is not running."""

    import os

    if os.popen("ps -a | grep NIDAQserver").read() == "" or not os.path.exists("/tmp/NIDAQserver"):
        raise ServerNotRunning()

    #The log file is a sequence of key=value pairs defining the settings the NIDAQserver is configured with
    #The easiest way to parse the file is to execute it as it is a valid python script. Note that security's not
    # a concern here.
    settings = {}
    log = open("/tmp/NIDAQserver/log","r")
    exec log.read() in settings
    samplesPerChannel = settings['samplesperchan']
    numberOfChannels = len(settings['channels'].split(', '))
    

    def read(samples=1):
        """Return a channels * /samples/ numpy array containing the /samples/ latest readings from the NIDAQ
        (the most recent reading is at index 0). For example, to access the 5th latest value of the third analog
        channel (Ai2), type: read(5)[4][2]. For most applications, pulling a single sample is sufficient."""

        binaryStream = open("/tmp/NIDAQserver/binary", "rb")
        chunk = binaryStream.read(samplesPerChannel * numberOfChannels * 8) # /numberOfChannels/ channels of 64 bits (8 bytes) doubles
        binaryStream.close() # We open and close the FIFO pipe each time to force the kernel to flush it, ensuring we have the latest data
        array = numpy.fromstring(chunk, numpy.float64, samplesPerChannel * numberOfChannels)
        array.shape = (array.size / numberOfChannels, numberOfChannels)
        return array[:samples]

    return read

def GetLR():
    """Return the left and right offsets of the robot in a tuple / 2-dimensional array."""
    global read
    #We first run the data through a median filter to avoid spikes in the readings.
    samples = read(8)
    samples.sort(0)
    median = samples[4]

    #Converts the first four voltages to distances; assumes that l1, l2, r1, r2 are
    #respectively connected to AI1 (Analog Input 1), AI2, AI0 and AI3 on the NIDAQ.
    r1,l1,l2,r2 = VoltageToDistance(median[:4])

    return GetOffset(l1,l2,r1,r2)

def VoltageToDistance(v):
    """Convert the voltage (V) at the leads of a Sharp GP2D12 IR Sensor to a distance in meters.
    Reliable only when the distance is between 0.01 and 0.08 meters. Works on numpy arrays as well as scalars."""

    return numpy.exp(numpy.log(142.1/v) / 0.88) / 1000.0

def GetOffset(l1, l2, r1, r2):
    """Return a two-dimensional matrix of offsets calculated from four scalars (or four 1 dimensional vectors of identical size),
    l1, l2, r1,r2 as described in the paper at [put link here]."""

    ANGLE = 50 * math.pi / 180.0 #This is a predefined constant linked to the plastic sensor mount.
    #If a new sensor mount is manufactured, be sure to update this constant (it corresponds to the angle alpha on the paper
    #mentionned in this function's docstring).

    l = l1 * l2 * numpy.sin(ANGLE) / numpy.sqrt(l1**2 + l2**2 - 2*l1*l2*numpy.cos(ANGLE))
    r = r1 * r2 * numpy.sin(ANGLE) / numpy.sqrt(r1**2 + r2**2 - 2*r1*r2*numpy.cos(ANGLE))
    return numpy.array([l,r])

