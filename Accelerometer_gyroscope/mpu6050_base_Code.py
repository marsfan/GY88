#mpu6050 library 1.0: basic data output. This file does not use the DMP system. Using that is complicated. 
#the only existing code for that is either arduino, C++, or pre built by the manufacturer.
#if I can figure out more about using the DMP, i will release a new version

#import smbus for i2c and math for the trig calculations
import smbus, math

bus = smbus.SMBus(1)
#set address of MPU6050
addr = 0x68

#set the power mgmnt registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


#set acclerometer scale values for when changing acclerometer full scale value (coming soon!)
ascale = 16384.0


#read unsigned 16 bit value
def readU16(reg):
	high = bus.read_byte_data(addr, reg)
	low = bus.read_byte_data(addr, reg + 1)
	val = (high << 8) + low
	return val
    
#read signed 16 bit value
def readS16(reg):
	val = readU16(reg)
	#might need to change to 
	#if result > 32767: result -= 65536
	if (val >= 0x8000):
		return ((65535 - val) + 1)
	else:
		return val
      
 #read data from accelrometer, convert to scaled form based on value ascale
def AX():
	x = readS16(0x3B)
	ax = x / ascale
	return ax
	
def AY():
	y = readS16(0x3D)
	ay = y / ascale
	return ay
	
def AZ():	
	z = readS16(0x3F)
	az = z / ascale
	return az

def GX():
	print("A")
	
def GY():
	print("A")
	
def GZ():
      print("A")
