# There are 2 approaches we can take for handling simultaneous events
# One: we could make every effect a class and store the current state (frame) of each effect and just tick up the frames until done
# Use this in a queue where we just call nextframe() on each effect until it is done and removed from the queue

# Two: We could use multithreading where it waits for events and set
# Ex: event = threading.Event()             event.set()



# This class takes in a transmitter object (so that the buffer knows where to get written to)
class Effect():
    #NOTE ALL EFFECTS MUST HAVE A START AND STOP ATTRIBUTE
    def __init__(self, transmitter):
        self.status = False
        self.counter = 0
        self.transmitter = transmitter

    def generateFrame(self):
        raise NotImplementedError

#TODO: in the other effects, implement the ability to change the start and stop positions