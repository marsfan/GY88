import smbus
bus = smbus.SMBus(1)
addr = 0x68
pwr_mgmnt_1 = 0x6B

#create a function to write one bit to a register
def writeBit(devAddr, regAddr, bitNum, data):
   bb = bus.read_i2c_block_data(devAddr, regAddr, 1)
   b = bb[0]
   if  (data != 0):
    b = (b | (1 << bitNum))
   else :
    b =  (b & ~(1 << bitNum))
   bus.write_byte_data(devAddr,regAddr,b)
   print()

#set up the mpu 6050
def init():
	writeBit(addr, pwr_mgmnt_1, 0, 1)
	writeBit(addr, pwr_mgmnt_1, 1, 0)
	writeBit(addr, pwr_mgmnt_1, 2, 0)
	print(bus.read_byte_data(addr, pwr_mgmnt_1))

#def dmpInit():
	#reset the device
init()
