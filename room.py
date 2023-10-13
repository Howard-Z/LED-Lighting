from transmitter import Transmitter

class Room():
    def __init__(self):
        self.dev_list = []

    def add_dev(self, ip, num_leds):
        new_dev = Transmitter(ip, num_leds)
        self.dev_list.append(new_dev)

    def run(self):
        try:
            while(True):
                for dev in self.dev_list:
                    dev.gen_buff()
                    dev.transmit()
        except KeyboardInterrupt:
            print("\nStopped")