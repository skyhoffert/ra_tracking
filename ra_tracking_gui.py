# File:		ra_tracking.py
# Written By:	Skylar Hoffert
# Modified:	2016_1031
# Description:	gui for tracking objects with pyephem
# Dependencies:	pyephem, pyqt4

import sys
import datetime
import math
import ephem
import threading
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# ****************************************************************************
# constants
APP_WIDTH = 720
APP_HEIGHT = 480
APP_NAME = "Tracking"

# ground station constants
gs_lon = -80.439639 * math.pi / 180
gs_lat = 37.229852 * math.pi / 180
# altitude above sea level
gs_elev = 620

# time between updates, in seconds
UPDATE_PERIOD = 1

# for the labels
LABEL_ELEV_PRE = "Elevation Angle: "
LABEL_AZ_PRE = "Azimuth Angle: "
LABEL_TXT_FONT = "Arial"
LABEL_TXT_SIZE = 12

# margins
MARGIN_STD = 4
MARGIN_OUTSIDE = APP_WIDTH / 16

# position of widgets
BTN_CALCULATE_WIDTH = 128
LBL_STD_WIDTH = APP_WIDTH - MARGIN_OUTSIDE*2
LBL_STD_HEIGHT = 24

# other utility vars
NO_TARGET = "no_target"

# ****************************************************************************
# global variables
gs_observer = ephem.Observer()

# ****************************************************************************
# functions
# Description:	Return the appropriate ephem object
# Inputs:	str = string containing the ephem object name
def find_ephem_obj( str ):
	if ( not str ):
		return
	if ( str == "moon" ):
		return ephem.Moon()
	elif ( str == "sun" ):
		return ephem.Sun()
	elif ( str == "mars" ):
		return ephem.Mars()
	elif ( str == "andromeda" or str == "m31" ):
		return ephem.readdb( "M31,f|G,0:42:44,+41:16:8,4.16,2000,11433|3700|35" )
	else:
		try:
			obj =  ephem.star( str )
		except KeyError:
			return None

def calculate():
	gs_lon = float(txt_lon.text()) * math.pi / 180
	gs_lat = float(txt_lat.text()) * math.pi / 180
	gs_observer.lat = gs_lat
	gs_observer.lon = gs_lon
	obj_to_track = find_ephem_obj(txt_obj_name.text())
	if ( obj_to_track ):
		gs_observer.date = datetime.datetime.utcnow()
		obj_to_track.compute(gs_observer)
		label_name.setText(obj_to_track.name)
		label_elev.setText("{} {}".format(LABEL_ELEV_PRE, obj_to_track.alt))
		label_az.setText("{} {}".format(LABEL_AZ_PRE, obj_to_track.az))
	else:
		label_name.setText(NO_TARGET)
		label_elev.setText("{} {}".format(LABEL_ELEV_PRE, NO_TARGET))
		label_az.setText("{} {}".format(LABEL_AZ_PRE, NO_TARGET))

def build_label( lbl, posx, posy, wid, ht, font , txt ):
	lbl.move(posx, posy)
	lbl.resize(wid, ht)
	lbl.setFont(font)
	lbl.setText(txt)


# ****************************************************************************
# main program

# set up the application
app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle(APP_NAME)
w.resize(APP_WIDTH, APP_HEIGHT)

# create font
txt_font = QFont(LABEL_TXT_FONT, LABEL_TXT_SIZE, QFont.Bold)

# init the ground station
gs_observer.lat = gs_lat
gs_observer.lon = gs_lon
gs_observer.elevation = gs_elev

# set up GUI components
# textbox for entry
txt_obj_name = QLineEdit(w)
txt_obj_name.move(MARGIN_OUTSIDE, APP_HEIGHT - MARGIN_OUTSIDE)
txt_obj_name.resize(LBL_STD_WIDTH - BTN_CALCULATE_WIDTH - MARGIN_STD, LBL_STD_HEIGHT)
txt_obj_name.returnPressed.connect(calculate)

# textboxes for gs lat
txt_lat = QLineEdit(w)
txt_lat.move(MARGIN_OUTSIDE + LBL_STD_WIDTH/4 + MARGIN_STD, APP_HEIGHT - MARGIN_OUTSIDE - LBL_STD_HEIGHT*3 - MARGIN_STD*3)
txt_lat.resize(LBL_STD_WIDTH/4, LBL_STD_HEIGHT)
txt_lat.returnPressed.connect(calculate)
txt_lat.setText(str(gs_lat * 180 / math.pi))

txt_lon = QLineEdit(w)
txt_lon.move(MARGIN_OUTSIDE + LBL_STD_WIDTH/4 + MARGIN_STD, APP_HEIGHT - MARGIN_OUTSIDE - LBL_STD_HEIGHT*2 - MARGIN_STD*2)
txt_lon.resize(LBL_STD_WIDTH/4, LBL_STD_HEIGHT)
txt_lon.returnPressed.connect(calculate)
txt_lon.setText(str(gs_lon * 180 / math.pi))

# build the labels
label_name = QLabel(w)
build_label(label_name, MARGIN_OUTSIDE, MARGIN_OUTSIDE, LBL_STD_WIDTH, LBL_STD_HEIGHT, txt_font, "Push calculate to go!")
label_elev = QLabel(w)
build_label(label_elev, MARGIN_OUTSIDE, MARGIN_OUTSIDE + LBL_STD_HEIGHT + MARGIN_STD, LBL_STD_WIDTH, LBL_STD_HEIGHT, txt_font, "{} {}".format(LABEL_ELEV_PRE, NO_TARGET))
label_az = QLabel(w)
build_label(label_az, MARGIN_OUTSIDE, MARGIN_OUTSIDE + LBL_STD_HEIGHT*2 + MARGIN_STD*2, LBL_STD_WIDTH, LBL_STD_HEIGHT, txt_font, "{} {}".format(LABEL_AZ_PRE, NO_TARGET))
label_desc = QLabel(w)
build_label(label_desc, MARGIN_OUTSIDE, APP_HEIGHT - MARGIN_OUTSIDE - LBL_STD_HEIGHT - MARGIN_STD, LBL_STD_WIDTH, LBL_STD_HEIGHT, txt_font, "Astronomical Object to be Tracked")
# gs labels
label_desc_gs = QLabel(w)
build_label(label_desc_gs, MARGIN_OUTSIDE, APP_HEIGHT - MARGIN_OUTSIDE - LBL_STD_HEIGHT*4 - MARGIN_STD*4, LBL_STD_WIDTH, LBL_STD_HEIGHT, txt_font, "Ground Station Location")
label_gs_lat = QLabel(w)
build_label(label_gs_lat, MARGIN_OUTSIDE, APP_HEIGHT - MARGIN_OUTSIDE - LBL_STD_HEIGHT*3 - MARGIN_STD*3, LBL_STD_WIDTH/4, LBL_STD_HEIGHT, txt_font, "Latitude:")
label_gs_lon = QLabel(w)
build_label(label_gs_lon, MARGIN_OUTSIDE, APP_HEIGHT - MARGIN_OUTSIDE - LBL_STD_HEIGHT*2 - MARGIN_STD*2, LBL_STD_WIDTH/4, LBL_STD_HEIGHT, txt_font, "Longitude:")

# calculate button
btn_calculate = QPushButton("Calculate", w)
btn_calculate.resize(BTN_CALCULATE_WIDTH, LBL_STD_HEIGHT)
btn_calculate.move(APP_WIDTH - MARGIN_OUTSIDE - BTN_CALCULATE_WIDTH, APP_HEIGHT - MARGIN_OUTSIDE)
btn_calculate.clicked.connect(calculate)

# other pretty stuff
painter = QPainter()
painter.begin(w)

pen = QPen(Qt.black, 2, Qt.SolidLine)
painter.setPen(pen)
painter.drawLine(20, 20, 200, 50)

painter.end()

timer = QTimer()
timer.timeout.connect(calculate)
timer.start(1000)

w.show()
app.exec_()

