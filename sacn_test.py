import numpy as np
from transmitter import Transmitter


# trans = Transmitter("192.168.1.134", 300)
# test_tup = (255, 255, 255, 255, 255, 255)
# arr = np.zeros(6, dtype=np.ubyte)
# for i in range(len(arr)):
#     arr[i] = 255

# def converter(data):
#     return tuple(i.item() for i in data)


# print(type(int(arr[0])))
# print(type(test_tup[0]))
# print(tuple(arr) == test_tup)
# print(type(tuple(arr)))
# print(type(test_tup))
# trans.transmit(converter(arr), 3)
# trans.transmit(test_tup, 3)
# trans.stop()

def pos_calc(length, trail, duration, counter, index):
    return int(((length * 3 + trail * 3)//duration * 3) * counter) - index * 3

for i in range(10):
    print(pos_calc(300, 50, 100, i, 0))