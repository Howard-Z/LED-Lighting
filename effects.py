import numpy as np
#from transmitter import Transmitter
import time


# There are 2 approaches we can take for handling simultaneous events
# One: we could make every effect a class and store the current state (frame) of each effect and just tick up the frames until done
# Use this in a queue where we just call nextframe() on each effect until it is done and removed from the queue

# Two: We could use multithreading where it waits for events and set
# Ex: event = threading.Event()             event.set()



# This class takes in a transmitter object (so that the buffer knows where to get written to)
class Effect():
    def __init__(self, transmitter):
        self.status = False
        self.counter = 0
        self.transmitter = transmitter

    def generateFrame(self):
        raise NotImplementedError


    def transmit(self, data):
        # we are going to assume that the input data will be an array of ints [r_1, g_1, b_1, r_2, g_2, b_2, ...]
        self.transmitter.transmit(tuple(data))


class Wipe(Effect):
    # This effect was meant for 1D strips
    # Does a wipe effect with a start pixel, end pixel, trail length, direction (left or right), and duration in frames
    def __init__(self, transmitter, start, stop, trail, color, direction, duration):
        super().__init__(transmitter)
        self.start = start
        self.stop = stop
        self.length = stop - start
        self.trail = trail
        self.direction = direction
        self.duration = duration
        self.color = color

        self.buffer = np.zeros((self.stop - self.start + self.trail)*3, dtype=np.ubyte)


    def clearBuffer(self):
        self.buffer.fill(0)

    def calculateBrightness(self, index):
        return ((1.0/self.trail) * (self.trail - index))

    def generateFrame(self):
        self.clearBuffer()
        pos2 = 0
        if self.direction:
            pos2 = int(((self.length + self.trail) * 3/self.duration) * self.counter)
            pos2 = pos2 - (pos2 % 3)
        else:
            pos2 = int(((self.length + self.trail) * 3/self.duration) * self.counter)
            pos2 = pos2 - (pos2 % 3)
        for i in range(self.trail):
            if self.direction:
                #had a really weird bug that was causing problems so this pos = pos2 thing is here
                pos = pos2 - i * 3
                if pos >= 0 and pos < ((self.length + self.trail) * 3) - 1:
                    self.buffer[pos] = int(self.calculateBrightness(i) * self.color[0])
                    self.buffer[pos + 1] = int(self.calculateBrightness(i) * self.color[1])
                    self.buffer[pos + 2] = int(self.calculateBrightness(i) * self.color[2])
            else:
                pos = (self.length) * 3 - (pos2 - i * 3)
                print(pos)
                if pos >= 0 and pos < ((self.length + self.trail) * 3) - 1:
                    self.buffer[pos] = int(self.calculateBrightness(i) * self.color[0])
                    self.buffer[pos + 1] = int(self.calculateBrightness(i) * self.color[1])
                    self.buffer[pos + 2] = int(self.calculateBrightness(i) * self.color[2])
        if self.counter >= self.duration:
            self.status = True
        self.counter += 1
        return self.buffer[:self.length * 3:]
    
    def transmit(self):
        super().transmit(self.buffer)
        return
