import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import csv
from dateutil import parser

x = []
y = []

with open('tempchart', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)


count = 0
#for i in data:
#    new = datetime.datetime.strptime(i[0], '%Y-%m-%d %H:%M:%S').date()
#    data[count][0] = new
#    count += 1

for i in data:
    new = parser.parse(i[0]).strftime('%Y%m%d%H%M%S')
    new = mdates.datestr2num(i[0])
    data[count][0] = new
    count += 1

for i in data:
    x.append(i[0])

for i in data:
    y.append(i[1])


plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(byminute=range(60), interval=5))
plt.plot_date(x, y, fmt="bo", tz=None, xdate=True)

plt.show()
