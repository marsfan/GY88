#mpu6050 library 1.0: basic data output. This file does not use the DMP system. Using that is complicated. 
#the only existing code for that is either arduino, C++, or pre built by the manufacturer.
#if I can figure out more about using the DMP, i will release a new version

#import smbus for i2c and math for the trig calculations
import smbus, math
