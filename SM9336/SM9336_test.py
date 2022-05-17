from SM9336 import *
from smbus2 import SMBus
import time
import datetime

time_inrement = 0.0005

i2c_bus = SMBus(1)

sensor = SM9336(i2c_bus)

time_a = time.time()
time_start = time.time()
loops=0
while (True):
	while (time.time() - time_a < time_inrement):
		time.sleep(0.00001)
	
	time_a += time_inrement
	p =sensor.get_reading()
	loops+=1
	
	if (loops % 100 == 0):
		print (loops, time.time()-time_start, p , (time.time()-time_start) / loops)
	
