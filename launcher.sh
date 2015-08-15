#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /home/pi/logger

sudo python gpstime.py

sudo python log-script.py

