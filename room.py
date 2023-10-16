from transmitter import Transmitter
import threading

class Room():
    def __init__(self):
        self.dev_list = []

    def add_dev(self, ip, num_leds):
        new_dev = Transmitter(ip, num_leds)
        self.dev_list.append(new_dev)

    def run(self):
        try:
            for dev in self.dev_list:
                t1 = threading.Thread(target=self.send, args=(dev,))
                t1.start()
        except KeyboardInterrupt:
            print("\nStopped")
    
    def send(self, dev):
        while(True):
            #TODO: Fix this to have the threads wait for the events queue to not be empty instead of spin locking
            if(dev.gen_buff() != False):
                dev.transmit()
            continue