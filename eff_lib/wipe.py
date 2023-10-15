from eff_lib.effects import Effect
import numpy as np


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
    