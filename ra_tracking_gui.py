# File:		ra_tracking.py
# Written By:	Skylar Hoffert
# Modified:	2016_1031
# Description:	gui for tracking objects with pyephem
# Dependencies:	pyephem, pyqt4

import sys
import datetime
import math
import ephem
from PyQt4.QtGui import *

# ****************************************************************************
# constants
APP_WIDTH = 640
APP_HEIGHT = 480
APP_NAME = "Tracking"

# ground station constants
GS_LON = -80.439639 * math.pi / 180
GS_LAT = 37.229852 * math.pi / 180
# altitude above sea level
GS_ELEV = 620

# time between updates, in seconds
UPDATE_PERIOD = 1

# for the labels
LABEL_ELEV_PRE = "Elevation Angle: "
LABEL_AZ_PRE = "Azimuth Angle: "
LABEL_TXT_FONT = "Arial"
LABEL_TXT_SIZE = 12

# margins
MARGIN_STD = 4

# position of widgets
BTN_CALCULATE_POS_X = APP_WIDTH / 8
BTN_CALCULATE_POS_Y = APP_HEIGHT / 4
BTN_CALCULATE_WIDTH = 128
BTN_CALCULATE_HEIGHT = 32
TXT_OBJ_NAME_POS_X = APP_WIDTH / 8
TXT_OBJ_NAME_POS_Y = APP_HEIGHT / 4 - BTN_CALCULATE_HEIGHT - MARGIN_STD 
LBL_STD_WIDTH = APP_WIDTH * 3 / 4
LBL_STD_HEIGHT = 24
LBL_INSTR_POS_X = APP_WIDTH / 8
LBL_INSTR_POS_Y = APP_HEIGHT / 8 - LBL_STD_HEIGHT - MARGIN_STD
LBL_NAME_POS_X = APP_WIDTH / 8
LBL_NAME_POS_Y = APP_HEIGHT / 4 + LBL_STD_HEIGHT * 4

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
	if ( str == "moon" ):
		return ephem.Moon()
	elif ( str == "sun" ):
		return ephem.Sun()
	elif ( str == "mars" ):
		return ephem.Mars()
	elif ( str == "andromeda" or str == "m31" ):
		return ephem.readdb( "M31,f|G,0:42:44,+41:16:8,4.16,2000,11433|3700|35" )
	else:
		return ephem.star( str )

def calculate():
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
gs_observer.lat = GS_LAT
gs_observer.lon = GS_LON
gs_observer.elevation = GS_ELEV

# set up GUI components
# textbox for entry
txt_obj_name = QLineEdit(w)
txt_obj_name.move(TXT_OBJ_NAME_POS_X, TXT_OBJ_NAME_POS_Y)
txt_obj_name.resize(LBL_STD_WIDTH, 32)

# build the labels
label_name = QLabel(w)
label_name.move(LBL_NAME_POS_X, LBL_NAME_POS_Y)
label_name.resize(LBL_STD_WIDTH, LBL_STD_HEIGHT)
label_name.setText("Push calculate to go!")
label_name.setFont(txt_font)
label_elev = QLabel(w)
label_elev.move(128,268)
label_elev.resize(LBL_STD_WIDTH, LBL_STD_HEIGHT)
label_elev.setText("{} {}".format(LABEL_ELEV_PRE, NO_TARGET))
label_elev.setFont(txt_font)
label_az = QLabel(w)
label_az.move(128,292)
label_az.resize(LBL_STD_WIDTH, LBL_STD_HEIGHT)
label_az.setText("{} {}".format(LABEL_AZ_PRE, NO_TARGET))
label_az.setFont(txt_font)

# calculate button
btn_calculate = QPushButton("Calculate", w)
btn_calculate.resize(BTN_CALCULATE_WIDTH, BTN_CALCULATE_HEIGHT)
btn_calculate.move(BTN_CALCULATE_POS_X, BTN_CALCULATE_POS_Y)
btn_calculate.clicked.connect(calculate)

w.show()
app.exec_()

