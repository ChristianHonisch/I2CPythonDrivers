from MC3479 import *
from smbus2 import SMBus
import time


i2c_bus = SMBus(5)

accelerometer = MC3479(i2c_bus)

while (True):
	acc_measurement = accelerometer.read_acceleration()
	print (acc_measurement)
	time.sleep(0.05)
