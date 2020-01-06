# PicturesAndPlaces
A collection of scripts for logging GPS data and taking periodic / timelapse photos via webcam on a Raspberry Pi. Intended for use in vehicles on roadtrips.

This code is a one-off project written over a couple weeks in preparation for a road trip way out west. I apologize for the mess.

You can read more at my website: http://wiki.exceedindustries.net/index.php?title=GPS_logger_%26_time_lapse_image_device


# Hardware
- Raspberry Pi Model B
  - Running latest Raspbian
- BU-353 S4 USB GPS Reciever
- Logitech C270 HD webcam
- A nice univeral car charger with a USB port

# Dependencies
sudo apt-get install gpsd gpsd-clients python-gps sqlite3 fswebcam

# GPS Install and Test
1. Install the dependencies as listed above.
2. Plug in the GPS unit to an open USB port. Be near a window, or better yet, outdoors.
3. Open a terminal and:
	- Run dmesg to see the device name of your GPS (likely /dev/ttyUSB0)
	- Run cgps and/or xgps to verify GPS functionality

# Camera Install and Test
1. Assuming you've installed the dependencies...
2. Plug in the webcam to an open USB port
3. Run fswebacm and adjust camera
4. Tip: Try experimenting with the -S flag of fswebcam. It tells your camera to take a few pictures, but only returns the last one taken. This allows your webcam to auto-focus and/or adjust light levels. I've found a value between 3-10 is about right; it all depends on the webcam in use.

# Raspberry Pi Specific
sudo pip install RPi.GPIO

## Edit /etc/default/gpsd:
```
START_DAEMON="true"
GPSD_OPTIONS="/dev/ttyUSB0"
```

## Create /home/pi/launcher.sh:
```sh
#!/bin/sh
# launcher.sh
# You can cd or skip the next line and add the full path to the last line
# but be careful if your script relies on relative paths?
cd /home/pi/logger
sudo python your_script.py
```

## Edit /etc/xdg/lxsession/LXDE-pi/autostart:
Add to the bottom:
```
@lxterminal -e /home/pi/launcher.sh
```
