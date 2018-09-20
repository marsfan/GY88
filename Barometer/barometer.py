# basic barometer reading script by gabriel roper 2/14/2014
# todo add system that gets ip address and barometric pressure to find altitude. using http://www.ip2location.com/python.aspx and https://code.google.com/p/python-weather-api/
# todo add ability for external programs to tell program rounding values
import smbus
import time
# import pygame will use later for visuals
# set i2c bus and barometer address
bus = smbus.SMBus(1)
addr = 0x77
# oversampling setting
oss = 1


def set_oss(value):
    global oss
    oss = value


# read 16 bytes from register requested
def read(address):
    bus.write_byte(addr, address)
    msb = bus.read_byte(addr)
    lsb = bus.read_byte(addr)
    return (msb << 8) + lsb


# read signed variables 16bytes
def reads(address):
    result = read(address)
    # might need to change to this, based on what I see.
    # if result > 32767: result -= 65536
    if (result >= 0x8000):
        return -((65535 - result) + 1)
    else:
        return result


# read calibration values
ac1 = reads(0xAA)
ac2 = reads(0xAC)
ac3 = reads(0xAE)
ac4 = read(0xB0)
ac5 = read(0xB2)
ac6 = read(0xB4)
b1 = reads(0xB6)
b2 = reads(0xB8)
mb = reads(0xBA)
mc = reads(0xBC)
md = reads(0xBE)


# read uncomensated tempature
def ut():
    bus.write_byte_data(addr, 0xF4, 0x2E)
    time.sleep(.005)
    hi = bus.read_byte_data(addr, 0xF6)
    lo = bus.read_byte_data(addr, 0xF7)
    result = (hi << 8) + lo

    return result


# read uncompensated pressure
def up():
    bus.write_byte_data(addr, 0xF4, (0x34 + (oss << 6)))
    time.sleep(.002 + (.003 * (2 ** oss)))
    msb = bus.read_byte_data(addr, 0xF6)
    lsb = bus.read_byte_data(addr, 0xF7)
    xlsb = bus.read_byte_data(addr, 0xF8)
    up = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - oss)
    return up


# calibrade temp
def cal_temp():
    x1 = (ut() - ac6) * ac5 / (2 ** 15)
    x2 = mc * (2 ** 11) / (x1 + md)
    b5 = x1 + x2
    t = (b5 + 8) / (2 ** 4)
    return t

    # calibrate pressure


def cal_press():
    # redo temp calibrations to get b5
    x1 = (ut() - ac6) * ac5 / (2 ** 15)
    x2 = mc * (2 ** 11) / (x1 + md)
    b5 = x1 + x2
    b6 = b5 - 4000
    x1 = (b2 * (b6 * b6 / (2 ** 12))) / (2 ** 11)
    x2 = ac2 * b6 / (2 ** 11)
    x3 = x1 + x2
    b3 = ((((ac1 * 4 + x3) << oss) + 2) / 4)
    x1 = ac3 * b6 / (2 ** 13)
    x2 = (b1 * (b6 * b6 / (2 ** 12))) / (2 ** 16)
    x3 = ((x1 + x2) + 2) / (2 ** 2)
    b4 = ac4 * (x3 + 32768) / (2 ** 15)
    b7 = (up() - b3) * (50000 >> oss)

    if(b7 < 0x800000000):
        p = (b7 * 2) / b4
    else:
        p = (b7 / b4) * 2
    x1 = (p / (2 ** 8)) * (p / (2 ** 8))
    x1 = (x1 * 3038) / (2 ** 16)
    x1 = (-7357 * p) / (2 ** 16)
    p = p + (x1 + x2 + 3791) / (2 ** 4)

    return p

    # does not work


def altitude(baro):
    return 44330 * (1 - (cal_press() / (baro * 3386.389))**(1 / 5.255))


def tempc():
    return cal_temp() / float(10)


def tempf():
    return tempc() * float(1.8) + 32


def presspa():
    return cal_press()


def presshpa():
    return presspa() / float(1000)


def pressinhg():
    return round(presspa() / float(3386.389), 2)


def pressmbar():
    return presspa() / float(100)


def pressatm():
    return presspa() / float(101325)
