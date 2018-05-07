import os
os.system("sudo killall pigpiod")
os.system("sudo pigpiod")

import time
import HX711
import time
import math
import pigpio
import random
#import paho.mqtt.client as client

#client = mqtt.Client("scale_game")
#client.connect(broker, 1883, 60)
#client.loop_start()


pi = pigpio.pi()
s = None;

zero_point = 0;

NToTare = 10000
NToRead = 1000

k = 0.07460526315

targetM = 0
nGood = 0

def cbf(count, mode, reading):
   print(count, mode, reading)

#s = HX711.sensor(pi, DATA=20, CLOCK=21, mode=HX711.CH_B_GAIN_32, callback=cbf)
#s.set_mode(HX711.CH_A_GAIN_64)
#s.set_callback(None)

def setup():
	global s
	s = HX711.sensor(pi, DATA=20, CLOCK=21, mode=HX711.CH_B_GAIN_32, callback=cbf)
	s.set_mode(HX711.CH_A_GAIN_64)
	s.set_callback(None)

	time.sleep(1)
	tare_scale()

def read_raw():
	c, mode, reading = s.get_reading()
	return(reading)

def tare_scale():
	global zero_point
	sum = 0
	for i in range(NToTare):
		sum += read_raw()

	zero_point = sum/NToTare

	print("zero point: " + str(zero_point))

def get_mass():
	vSum = sum([read_raw() for i in range(NToRead)])
	return(k*((vSum/NToRead) - zero_point))

def sign(x):
	if(x > 0):
		return(1)
	if(x < 0):
		return(-1)
	return(0)

def fitInRange(x, a, b):
	if(x < a):
		return(a)
	if(x > b):
		return(b)
	return(x)

def startGame():
	global targetM, nGood

	targetM = 2000*random.random() + 500
	tare_scale()
	nGood = 0

def getGameStatus():
	global nGood

	m = get_mass()
	mA = m
	
	m = get_mass()
	#average in new mass value to estimate	
	mA = .9*mA + .1*m

#	print(mA - targetM)

	L = 60
	bar = list((2*L + 1)*' ')
	bar[L] = '|'
	massI = sign(mA - targetM)*((abs(mA - targetM)**.8)/10 + (abs(mA - targetM)**.5)/6) + L + .5
	error = (fitInRange(massI, 0, len(bar) - 1) - L - .5)/L

#	print(massI)
 	massI = int(fitInRange(massI, 0, len(bar) - 1))

	if(massI == L):
		nGood += 1
	else:
		nGood = 0

	bar[massI] = '*'
	gameString = "".join(bar)
	done = (nGood >= 10)
	return(gameString, done, error)

def playGame():
	startGame()
	while(True):
		status = getGameStatus()
		print(status[0])
		if(status[1]):
			break
