import time, smbus, math

bus = smbus.SMBus(1)
addr = 0x1E
pi = 3.141592653
xmax = 0
xmin = 0
ymax = 0
ymin = 0
xoffset = -144
yoffset = - 350

bus.write_byte_data(addr, 0x02, 0x00)

#todo adjust so that the M_drdy pin will trigger reading, making reading faster. Sgeet says it goes low when data is ready. need to chek
while (True):
#for i in range(0,250):
	xmsb = bus.read_byte_data(addr, 0x03)
	xlsb = bus.read_byte_data(addr, 0x04)
	zmsb = bus.read_byte_data(addr, 0x05)
	zlsb = bus.read_byte_data(addr, 0x06)
	ymsb = bus.read_byte_data(addr, 0x07)
	ylsb = bus.read_byte_data(addr, 0x08)
	x = xlsb + (xmsb << 8) 
	y = ylsb + (ymsb << 8)
	z = zlsb + (zmsb << 8)
	time.sleep(.250)
	#might need to switch to 
	#if result > 32767: result -= 65536
	if x > 32767: x = -((65535 - x) + 1)
	if y > 32767: y = -((65535 - y) + 1)
	if z > 32767: z = -((65535 - z) + 1)
	x = x - xoffset
	y = y - yoffset
	#todo: find z offset
#	print x, y, z
	heading = math.atan2(y, x)
	if heading < 0:
		heading += 2 * math.pi
	#if heading > 2 * math.pi:
#		heading -= 2 * math.pi
	heading = math.degrees(heading)	
	print heading
