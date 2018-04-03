import ephem
import datetime
import sys
import argparse
import urllib.request as urllib
import math


def compute_angles(date=None):
	# handle the date argument
	date = date if date is not None else datetime.datetime.now()

	# fetch the tle from celestrak online
	response = urllib.urlopen('http://www.celestrak.com/NORAD/elements/noaa.txt')
	html = response.read()

	# split the html by new lines
	# we want NOAA 19, which was these indices as of April 4th, 2018
	name = str(html).split('\\r\\n')[57]
	line1 = str(html).split('\\r\\n')[58]
	line2 = str(html).split('\\r\\n')[59]

	# read in the tle
	tle_rec = ephem.readtle(name, line1, line2)

	# make a new ephem observer
	BB = ephem.Observer()
	BB.lon = 37.2725
	BB.lat = -80.4327
	BB.elev = 400
	BB.date = date

	# compute the orbit trajectory stuff
	tle_rec.compute(BB)

	# find the next pass
	next_pass = BB.next_pass(tle_rec)

	# print results
	print('Next pass: ', str(next_pass[0]))

	# move the current time to the next pass
	BB.date = next_pass[0]
	tle_rec.compute(BB)

	alts  = []
	azs   = []
	times = []

	while tle_rec.alt > 0:
		# save results to list in radians
		alts.append(math.degrees(float(tle_rec.alt)))
		azs.append(math.degrees(float(tle_rec.az)))
		times.append(BB.date.datetime())

		# compute next second timestep
		BB.date = BB.date.datetime() + datetime.timedelta(seconds=1)
		# compute next pointing angle
		tle_rec.compute(BB)

	# return a tuple with the lists
	# format is (az, el, time)
	return (azs, alts, times)
