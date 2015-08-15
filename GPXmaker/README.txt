sqlite2GPX.py

Your sqlite DB's schema must be:
(Id, Time, Lat, Lon, Alt)
Where Id is auto-incremented, Time is a datetime string that looks like: "2015-08-13 23:13:49.414395", and Lat, Lon, and Alt are self-explanatory.

Usage:
Specify the filename of your sqlite DB and the output filename. The DB requires it's file extension, the filename requires none (this tool only writes GPX).

Example:
python sqlite2GPX.py trip01.sqlite Trip1

