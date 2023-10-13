import numpy as np

class Buffer():
    def __init__(self, num_leds):
        self.num_leds = num_leds
        self.buff = np.zeros(num_leds * 3, dtype=np.ubyte)

    def buff_clear(self):
        self.buff.fill(0)

