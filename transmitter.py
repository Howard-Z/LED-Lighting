import time
import sacn

def converter(data):
    return tuple(i.item() for i in data)

class Transmitter():
    def __init__(self, ip, num_leds):
        self.ip = ip
        self.num_leds = num_leds
        self.num_univ = self.num_leds // 170 + 1
        self.sacn = sacn.sACNsender()
        self.start()

    # def transmit(self, data):
    #     self.sacn.start()
    #     for i in range(1, self.num_univ):
    #         try:
    #             self.sacn.activate_output(i)
    #             self.sacn[i].multicast = False
    #             self.sacn[i].destination = self.ip
    #             chunk = [data[j : j + 170] for j in range(0, len(data), 170)][i - 1]
    #             print(chunk)
    #             self.sacn[i].dmx_data = chunk
    #         except:
    #             continue
    #     self.sacn.stop()

    # This function takes in self, data and duration
    # data: This is a tuple of integers 0-255 inclusive of length n
    # duration: This is the time in between each frame
    # TODO: convert this to use manual flush and lock at fixed fps
    def transmit(self, raw, duration):
        data = converter(raw)
        #self.sacn.start()
        for i in range(1, self.num_univ + 1):
            print("Universe {}".format(i))
            try:
                self.sacn.activate_output(i)
                self.sacn[i].multicast = False
                self.sacn[i].destination = self.ip
                chunk = [data[j : j + 510] for j in range(0, len(data), 510)][i - 1]
                print(chunk)
                self.sacn[i].dmx_data = chunk
            except:
                continue
        time.sleep(duration)
        #self.sacn.stop()

    def start(self):
        self.sacn.start()

    def stop(self):
        self.sacn.stop()