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
	obs = ephem.Observer()
	obs.lon = 37.2725
	obs.lat = -80.4327
	obs.elev = 400
	obs.date = date

	# compute the orbit trajectory stuff
	tle_rec.compute(obs)

	# find the next pass
	next_pass = obs.next_pass(tle_rec)

	# print results
	print('Next pass: ', str(next_pass[0]))

	# move the current time to the next pass
	obs.date = next_pass[0]
	tle_rec.compute(obs)

	# empty lists to start
	alts  = []
	azs   = []
	times = []

	# loop through entire pass
	while tle_rec.alt > 0:
		# save results to list in radians
		alts.append(math.degrees(float(tle_rec.alt)))
		azs.append(math.degrees(float(tle_rec.az)))
		times.append(obs.date.datetime())

		# compute next second timestep
		obs.date = obs.date.datetime() + datetime.timedelta(seconds=1)
		# compute next pointing angle
		tle_rec.compute(obs)

	# return a tuple with the lists
	# format is (az, el, time)
	return (azs, alts, times)
