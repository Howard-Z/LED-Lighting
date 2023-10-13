from transmitter import Transmitter
import threading
import concurrent.futures

class Room():
    def __init__(self):
        self.dev_list = []
        #self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=12)

    def add_dev(self, ip, num_leds):
        new_dev = Transmitter(ip, num_leds)
        self.dev_list.append(new_dev)

    def run(self):
        try:
            for dev in self.dev_list:
                #TODO: FIX THREADING PROBLEM HERE
                t1 = threading.Thread(target=self.send, args=(dev,))
                t1.start()
                #self.pool.submit(self.send(dev))
        except KeyboardInterrupt:
            print("\nStopped")
    
    def send(self, dev):
        while(True):
            if(dev.gen_buff() != False):
                dev.transmit()
            continue