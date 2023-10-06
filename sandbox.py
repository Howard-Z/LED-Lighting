import json
import requests

# There are 2 approaches we can take for handling simultaneous events
# One: we could make every effect a class and store the current state (frame) of each effect and just tick up the frames until done
# Use this in a queue where we just call nextframe() on each effect until it is done and removed from the queue

# Two: We could use multithreading where it waits for events and set
# Ex: event = threading.Event()             event.set()

def intToHexStr(num):
    num = hex(num)
    num = str(num)[2:]
    for i in range (6 - len(num)):
        num += "0"
    return num

class Effect():
    def __init__(self, ip):
        self.ip = ip
        self.status = False
        self.counter = 0

    def generateFrame(self):
        raise NotImplementedError


    def transmit(self, data):
        temp = {"seg":{"i":data}}
        print(temp)
        response = requests.post(
            f"http://{self.ip}/json",
            data=json.dumps(temp),
            headers={"Content-Type": "application/json"},
        )
        # Check if the request was successful
        if response.status_code != 200:
            print("Failed to toggle WLED power")

class Wipe(Effect):
    # This effect was meant for 1D strips
    # Does a wipe effect with a start pixel, end pixel, trail length, direction (left or right), and duration in frames
    def __init__(self, ip, start, stop, trail, direction, duration):
        super().__init__(ip)
        self.start = start
        self.stop = stop
        self.length = stop - start
        self.trail = trail
        self.direction = direction
        self.duration = duration
        #this is temp for testing
        self.buffer = [0] * (stop - start)

    def clearBuffer(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = intToHexStr(0)

    def calculateBrightness(self, index):
        return 1 - (1.0/self.trail) * index

    def generateFrame(self):
        self.clearBuffer()
        for i in range(self.trail):
            if self.direction:
                #debate on whether this minus one should be here, either it has an empty frame for a few frames or the last frame is the end of the tail at the end
                pos = (self.length + self.trail - 1)/self.duration * self.counter - i
                if pos >= 0 and pos < self.length:
                    #This is really stupid and should only be used in testing
                    hexnum = int(self.calculateBrightness(i) * 100)
                    self.buffer[int(pos)] = intToHexStr(hexnum)
        self.counter += 1
        if self.counter == self.duration:
            self.status = True
    def transmit(self):
        return super().transmit(self.buffer)

# eff = Wipe("192.168.1.121", 0, 329, 5, True, 100)
# while eff.status != True:
#     eff.generateFrame()
#     print(eff.buffer)