import NIDAQ
import numpy
import math
import time

class control:

    def __init__(self):
        self.index = 0
        self.time = time.time()
        self.AO = NIDAQ.AOTask()
        self.AO.start()

    def step(self, input_values):
        ai5 = input_values[5]
        ai6 = input_values[6]
        ai7 = input_values[7]
        self.index += 1
        sine_wave = (5.0/2) * (math.sin(float(self.index)/10.0) + 1)
        self.AO.write(numpy.array([sine_wave]))

        if self.index % 100 == 0:
            now = time.time()
            dt = now - self.time
            print 'dt=', dt/100.0
            self.time = now

