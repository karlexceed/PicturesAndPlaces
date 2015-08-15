import datetime
import gpxpy
import gpxpy.gpx
import sqlite3
import sys
import time


def main(dbsource, filename):
	real_filename = filename + '.gpx'
	gpx = gpxpy.gpx.GPX()
	
	# Create first track in our GPX:
	gpx_track = gpxpy.gpx.GPXTrack()
	gpx.tracks.append(gpx_track)
	
	# Create first segment in our GPX track:
	gpx_segment = gpxpy.gpx.GPXTrackSegment()
	gpx_track.segments.append(gpx_segment)
	
	# Read the DB and create points:
	try:
		con = sqlite3.connect(dbsource, detect_types=sqlite3.PARSE_DECLTYPES)
		
		cur = con.cursor()  
		
		lat = 0
		lon = 0
		alt = 0
		cur.execute('SELECT * FROM coordinates')
		
		for row in cur.fetchall():
			key_id, time_stmp, lat, lon, alt = row
			print 'Time: %s Lat: %s Lon: %s Alt: %s' % (time_stmp, lat, lon, alt)
			
			if key_id != 1:
				newtimestamp = datetime.datetime.strptime(time_stmp, '%Y-%m-%d %H:%M:%S.%f')
				#print newtimestamp
				newertimestamp = time.mktime(newtimestamp.timetuple())
				#print newertimestamp
				gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=alt, time=newtimestamp))
	
	except sqlite3.Error, e:
		if con:
			con.rollback()
		
		print "Error %s:" % e.args[0]
		sys.exit(1)
	
	finally:
		if con:
			con.close()
	
	
	foo = gpx.to_xml()
	
	f = open(real_filename, 'w')
	f.write(foo)
	
	print 'Done.'

if __name__ == "__main__":
	# call with 2 args, first is your DB, second is output filename (no type)
	main(sys.argv[1], sys.argv[2])

