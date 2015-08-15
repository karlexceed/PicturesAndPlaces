#! /usr/bin/python
#
# This program is designed to take a photo from a webcam once every 30 seconds
# as well as read, display, and log GPS coordinates every 5 seconds to a sqlite db.
# Oh, and it blinks an LED; 3 times at startup and then once for every good GPS fix
#
# Large parts written by:
# Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
#
# Other parts taken from:
# Rahul Kar at http://www.rpiblog.com/2012/09/using-gpio-of-raspberry-pi-to-blink-led.html
# Alex Martelli's answer on http://stackoverflow.com/questions/1829872/read-datetime-back-from-sqlite-as-a-datetime-in-python
# http://zetcode.com/db/sqlitepythontutorial/
#
# Cobbled together by:
# karlexceed - August 2015


import datetime
from gps import *
import os
import RPi.GPIO as GPIO
import sqlite3
import sys
import threading
import time

gpsd = None		# Seting the global variable

DB_NAME = 'gps_log_01.sqlite'

LED1 = 18	# GPIO 24
LED_TIMEOUT = 0.1

os.system('clear')	# Clear the terminal (optional)


class GpsPoller(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global gpsd		# Bring it in scope
		gpsd = gps(mode=WATCH_ENABLE)	# Starting the stream of info
		self.current_value = None
		self.running = True	# Setting the thread running to true

	def run(self):
		global gpsd
		while gpsp.running:
			gpsd.next()	# This will continue to loop and grab EACH set of gpsd info to clear the buffer

def log_to_db(lat=0, lon=0, alt=0):
	try:
		con = sqlite3.connect(DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES)

		cur = con.cursor()  
	
		nowish = datetime.datetime.now()
		cur.execute('insert into coordinates (Time, Lat, Lon, Alt) values(?, ?, ?, ?)', (datetime.datetime.now(), lat, lon, alt))

		con.commit()

	except sqlite3.Error, e:
		if con:
			con.rollback()

		print "Error %s:" % e.args[0]
		#sys.exit(1)

	finally:
		if con:
			con.close()

def take_and_save_image():
	
	os.system("fswebcam -r 1280x960 -S 10 --save ./images/%Y-%m-%d_%H:%M:%S.jpeg")

# Blinking function
def blink(pin):
	GPIO.output(pin, GPIO.HIGH)
	time.sleep(LED_TIMEOUT)
	GPIO.output(pin, GPIO.LOW)
	return

def blink3(pin):
	blink(pin)
	time.sleep(LED_TIMEOUT)
	blink(pin)
	time.sleep(LED_TIMEOUT)
	blink(pin)

if __name__ == '__main__':
	
	# Intro!!!1
	print """
		GPS AND IMAGE LOGGER
		karlexceed
		
		Large parts written by: Dan Mandle http://dan.mandle.me
	"""
	# To use Raspberry Pi board pin numbers
	GPIO.setmode(GPIO.BOARD)
	# Set up GPIO output channel
	GPIO.setup(LED1, GPIO.OUT)
	# Blink an LED 3 times
	blink3(LED1)
	time.sleep(1)
	
	gpsp = GpsPoller()	# Create the thread
	loop_counter = 0	# Let's count loops
	
	try:
		gpsp.start()	# Start it up
		while True:
			# It may take a second or two to get good data
			
			os.system('clear')
			
			print
			print ' GPS reading'
			print '----------------------------------------'
			print 'latitude    ' , gpsd.fix.latitude
			print 'longitude   ' , gpsd.fix.longitude
			print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
			print 'altitude (m)' , gpsd.fix.altitude
			print 'eps         ' , gpsd.fix.eps
			print 'epx         ' , gpsd.fix.epx
			print 'epv         ' , gpsd.fix.epv
			print 'ept         ' , gpsd.fix.ept
			print 'speed (m/s) ' , gpsd.fix.speed
			print 'climb       ' , gpsd.fix.climb
			print 'track       ' , gpsd.fix.track
			print 'mode        ' , gpsd.fix.mode
			print
			print 'sats        ' , gpsd.satellites
			
			# Log data if we have a (decent) fix
			if gpsd.fix.mode >= 2:
				log_to_db(gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude)
				blink(LED1)	# And let's blink while we're at it!
				
				if gpsd.fix.mode >= 3:	# Blink twice for 3D fix
					time.sleep(LED_TIMEOUT)
					blink(LED1)
			
			time.sleep(10)	# Set to whatever
			loop_counter += 1
			
			# Every 30 seconds (roughly) take a picture
			if loop_counter%3 == 0:
				take_and_save_image()
			
	except (KeyboardInterrupt, SystemExit):	# When you press ctrl+c
		print "\nKilling Thread..."
		
		GPIO.cleanup()		# Shutdown GPIO
		
		gpsp.running = False	# Kill it!
		gpsp.join()		# Wait for the thread to finish
		
	print "Done.\nExiting."

