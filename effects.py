import numpy as np
from transmitter import Transmitter



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
        self.transmitter.transmit(tuple(data), .025)

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
        #this is temp for testing
        self.buffer = np.zeros((self.stop - self.start)*3, dtype=np.ubyte)

    def clearBuffer(self):
        self.buffer.fill(0)

    def calculateBrightness(self, index):
        return ((1.0/self.trail) * (self.trail - index))

    def generateFrame(self):
        self.clearBuffer()
        for i in range(self.trail):
            if self.direction:
                #TODO fix bug where the effect doesn't finish
                pos = int(((self.length + self.trail)//self.duration) * self.counter)* 3 - i * 3
                if pos >= 0 and pos < (self.length - 1) * 3:
                    #print(pos)
                    self.buffer[pos] = int(self.calculateBrightness(i) * self.color[0])
                    self.buffer[pos + 1] = int(self.calculateBrightness(i) * self.color[1])
                    self.buffer[pos + 2] = int(self.calculateBrightness(i) * self.color[2])
        self.counter += 1
        print(self.counter)
        #TODO: fix issue with this timing in pos line
        if self.counter == self.duration:
            self.status = True
    
    def transmit(self):
        super().transmit(self.buffer)
        return

trans = Transmitter("192.168.1.134", 300)
eff = Wipe(trans, 0, 300, 1, (255, 255, 255), True, 100)
while(eff.status != True):
    eff.generateFrame()
    eff.transmit()
trans.stop()
