#################################################################
#																#
# 		Barebone code for sending signal to Netstation 			#
#																#
#################################################################

from __future__ import absolute_import, division
# import pandas as pd # these are for reading from excel files
# import random, os, glob, pylab
import numpy as np  # whole numpy lib is available, prepend 'np.'
# from numpy import (sin, cos, tan, log, log10, pi, average,
#                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
import os  # handy system and path functions
import sys  # to get file system encoding
import time
import logging
# import csv #useful for handling csv files

# from psychopy import visual, logging, core, event, data , sound, gui,locale_setup# import some libraries from PsychoPy
# from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                # STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
autolog=[]

import egi.simple as egi 
ms_localtime = egi.ms_localtime     
ns = egi.Netstation()
ns.connect('10.0.0.42', 55513)
ns.BeginSession()
ns.sync()
ns.StartRecording()
ns.sync()
ns.send_event(key='strt', timestamp=None,pad=False)

print "Imported PyNetstation and connected. Sending 5 'auto' events in +1 second increments. Type beep() for sending custom signal."

### For Logging 
# _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
# os.chdir(_thisDir)
# filename = _thisDir + os.sep + u'data/%s' % (ms_localtime())

# logFile = logging.LogFile(filename+'.log', level=logging.EXP)
# logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

ns.sync()

### Sample function for sending pulse: Type beep() 
def beep(): 
	ns.sync()
	log_time=egi.ms_localtime()
	# logging.data('beep sent at local time: ' + str(egi.ms_localtime()))
	print "Beep logged at " + str(log_time)
	ns.sync()
	sent_time=egi.ms_localtime()
	ns.send_event(key='beep', timestamp=None, description='below is sample table', table={'abcd' : 1, 'efgh' : 2}, pad=False)
	print "Beep sent at " + str(sent_time)
	diff = log_time - sent_time
	return diff

### Sample 10 incremental pulses sent to Netstation 
k = 2
time.sleep(k) 
for i in range(0,5):
	ns.sync()
	#logging.data('auto: ' + str(egi.ms_localtime()))
	print "auto logged at " + str(egi.ms_localtime())
	ns.send_event(key='auto', timestamp=None, description='below is sample table', table={'indx' : i, 'kinc' : k}, pad=False)
	autolog.append(egi.ms_localtime())
	print "auto sent at " + str(egi.ms_localtime())
	k += 1
	time.sleep(k)

np.savetxt('autolog.csv',autolog,delimiter=',',fmt='%d')





