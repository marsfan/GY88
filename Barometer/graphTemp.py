import datetime, sys, time, csv, barometer, matplotlib.pyplot as plt

temparray= []
x = 0


try:
    while True:
        f = open("data.csv", 'a')
        writer = csv.writer(f)
        dattime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temp = barometer.tempf()
        print(temp)
        print (x)
        x = x + 1
        writer.writerow( (dattime, temp) )
        temparray.append(temp)
        f.close()
        time.sleep(60)
	
	
	
except KeyboardInterrupt:
   pass

plt.plot(temparray)
plt.show()

sys.exit(0)
