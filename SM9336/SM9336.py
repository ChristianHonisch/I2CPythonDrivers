#! /usr/bin/python


import time
import math

from smbus2 import SMBus, i2c_msg

SM9336_TEMP_ADDRESS = 0x2E


class SM9336:

	def __init__(self, i2c_bus, SM9336_Address = 0x6C, SM9336_Address_CRC = 0x6D, Sensor_Fullscale = 250, debug_outputs = False):
		self.bus            = i2c_bus
		self.debug_outputs  = debug_outputs
		self.sensor_address = SM9336_Address
		self.fullscale      = Sensor_Fullscale * 1.25 #linear range: +-250 fullscale: +25%
		
		#From Datasheet: Thus, after power up it is necessary to wait until the 
		#STATUS.dsp_s_up and dsp_t_up bits have been set at least 
		#once before using the temperature or pressure data. It is
		#not sufficient to wait just for a fixed time delay
		
		#todo: wait until bits are set.

	def raw_to_val(self, value):
		if (value >32767):
			value = value - 65536
		return self.fullscale / 32768. * value

	def get_reading(self):
		
		command     = [SM9336_TEMP_ADDRESS]
		readcommand = i2c_msg.write(self.sensor_address,command)
		readbuffer  = i2c_msg.read(self.sensor_address,6)
		self.bus.i2c_rdwr(readcommand,readbuffer)
		
		pressure_raw  = ord(readbuffer.buf[3])<<8
		pressure_raw += ord(readbuffer.buf[2])
		temp_raw      = ord(readbuffer.buf[1])<<8
		temp_raw     += ord(readbuffer.buf[0])
		
		#todo: fix formula
		#C_TEMP = (temp_raw+16881.)/397.2 
		
		if (self.debug_outputs==True):
			print (readbuffer.buf[4], readbuffer.buf[5])
			print (pressure_raw,self.raw_to_val(pressure_raw), temp_raw)
		pressure_pa = self.raw_to_val(pressure_raw)
		if (self.debug_outputs==True):
			print (pressure_pa)
		return (pressure_pa)
