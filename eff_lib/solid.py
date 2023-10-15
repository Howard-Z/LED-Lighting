from eff_lib.effects import Effect
import numpy as np

class Solid(Effect):
    def __init__(self, transmitter, start, stop, attack, hold, decay, color):
        super().__init__(transmitter)
        self.start = start
        self.stop = stop
        self.length = start = stop
        self.attack = attack
        self.hold = hold
        self.decay = decay
        self.color = color
        self.duration = attack + hold + decay
        self.buffer = np.zeros((self.length) * 3, dtype=np.ubyte)

    def clearBuffer(self):
        self.buffer.fill(0)

    def att_bri(self):
        if self.counter == 0:
            return 0
        return self.counter/self.attack

    def dec_bri(self):
        bri = 1 - (self.counter - self.attack - self.hold + 1)/self.decay
        print(bri)
        return bri

    def generateFrame(self):
        self.clearBuffer()
        #Here we are in the decay area
        #if self.counter < self.attack + self.hold + self.decay:
        if self.counter >= self.attack + self.hold:
            bri = self.dec_bri()
            for i in range(0, self.length * 3, 3):
                self.buffer[i] = int(self.color[0] * bri)
                self.buffer[i + 1] = int(self.color[1] * bri)
                self.buffer[i + 2] = int(self.color[2] * bri)
        #Here we are in the hold area:
        elif self.counter >= self.attack:
            for i in range(0, self.length * 3, 3):
                self.buffer[i] = self.color[0]
                self.buffer[i + 1] = self.color[1]
                self.buffer[i + 2] = self.color[2]

        #Here we are in the in attack area
        else:
            bri = self.att_bri()
            for i in range(0, self.length * 3, 3):
                self.buffer[i] = int(self.color[0] * bri)
                self.buffer[i + 1] = int(self.color[1] * bri)
                self.buffer[i + 2] = int(self.color[2] * bri)
        self.counter += 1
        if self.counter >= self.duration:
            self.status = True
        #print(self.buffer)
        return self.buffer