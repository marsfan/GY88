import sys
import time
import barometer
import matplotlib.pyplot as plt

temparray = []
x = 0

try:
    while True:
        temp = barometer.tempf()
        print(temp)
        print(x)
        x = x + 1
        temparray.append(temp)
        time.sleep(1)


except KeyboardInterrupt:
    pass

plt.plot(temparray)
plt.show()

sys.exit(0)
