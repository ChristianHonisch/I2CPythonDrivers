#! /usr/bin/python


import time
import math

from smbus2 import SMBus, i2c_msg

MC3479_REG_MODE= 0x07
MC3479_MODE_WAKE = 0x01 #further mode: standby. further options: i2c wdt
MC3479_MODE_STANDBY = 0x00

MC3479_REG_SAMPLE_RATE = 0x08
MC3479_SAMPLE_RATE_25 = 0x10
MC3479_SAMPLE_RATE_100 = 0x13
MC3479_SAMPLE_RATE_125 = 0x14
MC3479_SAMPLE_RATE_250 = 0x15
MC3479_SAMPLE_RATE_1000 = 0x17


MC3479_REG_Range_Scale = 0x20
MC3479_Range_2g = 0x00
MC3479_Range_8g = 0x20
MC3479_Range_12g = 0x40
MC3479_LPF_Disabled = 0x00
MC3479_LPF_5 = 0x0D


MC3479_REG_ACCELEROMETER_OUT_X_LSB = 0x0D

class MC3479:
	def __init__(self, i2c_bus, MC3479_Address = 0x6C, debug_outputs=False):
		self.bus = i2c_bus
		self.debug_outputs=debug_outputs
		self.sensor_address = MC3479_Address
		
		command=[MC3479_REG_MODE, MC3479_MODE_STANDBY] #data sheet says: settings can only be changed in off mode.
		msg = i2c_msg.write(self.sensor_address, command)
		self.bus.i2c_rdwr(msg)
		time.sleep(0.01)
		
		command=[MC3479_REG_SAMPLE_RATE, MC3479_SAMPLE_RATE_25] 
		msg = i2c_msg.write(self.sensor_address, command)
		self.bus.i2c_rdwr(msg)
		time.sleep(0.01)
		
		command=[MC3479_REG_Range_Scale, MC3479_LPF_5 | MC3479_Range_8g]
		print (command)
		self.fullscale = 8.
		
		msg = i2c_msg.write(self.sensor_address, command)
		self.bus.i2c_rdwr(msg)
		time.sleep(0.01)
		
		command=[MC3479_REG_MODE, MC3479_MODE_WAKE] #enable, wdt off
		msg = i2c_msg.write(self.sensor_address, command)
		self.bus.i2c_rdwr(msg)
		time.sleep(0.1)
		
	def raw_to_val(self, value):
		if (value >32767):
			value = value - 65536
		return self.fullscale / 32768. * value
	
	def read_acceleration(self):
		command=[MC3479_REG_ACCELEROMETER_OUT_X_LSB]
		readcommand = i2c_msg.write(self.sensor_address,command)
		readbuffer=i2c_msg.read(self.sensor_address,6)
		self.bus.i2c_rdwr(readcommand,readbuffer)
		
		if (self.debug_outputs==True):
			for i in range (0,6):
				print(ord(readbuffer.buf[i]))
		
		x_raw = ord(readbuffer.buf[0]) + ord(readbuffer.buf[1])*256
		y_raw = ord(readbuffer.buf[2]) + ord(readbuffer.buf[3])*256
		z_raw = ord(readbuffer.buf[4]) + ord(readbuffer.buf[5])*256
		
		if (self.debug_outputs==True):
			print (x_raw, y_raw, z_raw)
		
		x= round (self.raw_to_val (x_raw ),4)
		y= round (self.raw_to_val (y_raw ),4)
		z= round (self.raw_to_val (z_raw ),4)
		return (x,y,z)
