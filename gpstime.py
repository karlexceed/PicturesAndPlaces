# From: http://code.google.com/p/gpstime/
# Modified with comment from BeJay at: https://www.raspberrypi.org/forums/viewtopic.php?t=28484&p=251845
#
# karlexceed - August 2015

import os
import RPi.GPIO as GPIO
import sys
import time
from gps import *

LED1 = 18	# GPIO 24
LED_TIMEOUT = 0.1

# Blinking function
def blink(pin):
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(LED_TIMEOUT)
	GPIO.output(pin,GPIO.LOW)
	return

def blink3(pin):
	blink(pin)
	time.sleep(LED_TIMEOUT)
	blink(pin)
	time.sleep(LED_TIMEOUT)
	blink(pin)

# Hack to address a bug
os.system('sudo killall gpsd')
os.system('sudo fake-hwclock load force')
#os.system('sudo date --set="20150801 12:34:56"')
os.system('sudo /etc/init.d/gpsd start')

print 'Sleep quick!'
time.sleep(5)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED1, GPIO.OUT)

# LED on!
GPIO.output(LED1,GPIO.HIGH)

print 'Attempting to access GPS time...'

try:
	gpsd = gps(mode=WATCH_ENABLE)
except:
	print 'No GPS connection present. TIME NOT SET.'
	sys.exit()

while True:
	gpsd.next()
	if gpsd.utc != None and gpsd.utc != '':
		# LED off!
		GPIO.output(LED1,GPIO.LOW)
		
		gpstime = gpsd.utc[0:4] + gpsd.utc[5:7] + gpsd.utc[8:10] + ' ' + gpsd.utc[11:19]
		print 'Setting system time to GPS time...'
		print gpstime
		os.system('sudo date --set="%s" -u' % gpstime)
		print 'System time set.'
		# Blink an LED
		blink3(LED1)
		sys.exit()
	time.sleep(1)

GPIO.cleanup()		# Shutdown GPIO
