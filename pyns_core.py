"""
This module contains functions to calculate average timing difference to test the synchronization of PsychoPy and NetStation logs.
Processing log info is segmented into 3 phases to add flexibility:
	- filter_log: mainly cleaning data
	- filter_event: filter data to user's event tags
	- timediff: computes time difference

There are 3 functions for each, PsychoPy and NetStation.

Order of processing:
1. PsychoPy:   filter_pylog --> filter_pyevent --> timediff_py
2. NetStation: filter_nslog --> filter_nsevent --> timediff_ns

Then use average_diff to compare two timestamps.

The second part measures and prints out timing difference for photocell timing in PsychoPy and NetStation machine

::Use pyns_run.py file to run as a whole::

Type help(function name) for function docstring. ie. help(filter_pylog)
"""
import csv
import time
import pandas as pd
import numpy as np
from decimal import Decimal


### Processing PsychoPy ###
def filter_pylog(filename,columnName):
	"""
	Syntax: filter_pylog('string of csv file name w/o extension','data')
	Example: filter_pylog('test2','data')

	This function is specific for PsychoPy log csv. It calls in the converted csv fileself.
	First cleans data with random '' and data types.
	Then filters out specific column data types.
	"""
	filtered_pylog=[]
	columnName=columnName.lower()
	csv_name=str(filename) + ".csv"
	with open(csv_name) as csvDataFile:
		pydata=list(csv.reader(csvDataFile))
	#clean out empty ' ' in data
	for i in range(0,len(pydata)):
		try:
			pydata[i][1]=pydata[i][1][:-1].lower()
		except IndexError:
			pass
	#convert from 'string of seconds' to 'float of milliseconds'
	for i in range(0,len(pydata)):
		try:
			pydata[i][0]=round(float(pydata[i][0])*1000,2)
		except ValueError:
			pass
	#filter out data by columnName
	for i in range(0,len(pydata)):
		try:
			if pydata[i][1]==str(columnName):
				filtered_pylog.append(pydata[i])
		except IndexError:
			pass
	return filtered_pylog


def filter_pyevent(filtered_pydata,*event_tags):
	"""
	Syntax: filter_pyevent(cleaned data from previous function filter_pylog,'event_tags1','event_tags2'...)
	Example: filter_pyevent(filtered_pylog,'int','ope','clo')

	This function takes in the resulted filtered data from previous function filter_pylog,
	and takes variable arguments with user specific event tags.
	Note that it reads the first three letters of the event tags as NetStation communication is limiting with 4 letters.
	"""
	filtered_pyevent=[]
	for event in event_tags:
		for i in range(0,len(filtered_pydata)):
			if filtered_pydata[i][2][0:3]==str(event):
				filtered_pyevent.append(filtered_pydata[i])
	filtered_pyevent=sorted(filtered_pyevent)
	return filtered_pyevent


def timediff_py(filtered_pyevent):
	"""
	Example: timediff_py(filtered_pyevent)

	This function takes in the sorted event list, and takes difference of every each item.
	Resulted time difference is in milliseconds.
	ie. item[1]-item[0], item[2]-item[1] ...
	"""
	diff_py=[]
	for i in range(0,len(filtered_pyevent)-1):
		k = round(filtered_pyevent[i+1][0]-filtered_pyevent[i][0],1)
		diff_py.append(k)
	return diff_py


### Processing NetStation ###
def filter_nslog(filename):
	"""
	Syntax: filter_nslog('string of csv file name w/o extension')
	Example: filter_nslog('test1')

	This function is specific for NetStation log csv. It calls in the converted csv.
	First cleans data with random '_' and converts HH:MM:SS:MS time format to milliseconds.
	"""
	csv_name=str(filename) + ".csv"
	with open(csv_name) as csvDataFile:
		nsdata=list(csv.reader(csvDataFile))
	#remove random '_' in front of time format
	for i in range(0,len(nsdata)):
		try:
			nsdata[i][4]=nsdata[i][4][1:]
		except IndexError:
			pass
	#convert from string of HH:MM:SS:MMM to MS
	for i in range(0,len(nsdata)):
		try:
			hh=int(nsdata[i][4][0:2]) * 3600000
			mm=int(nsdata[i][4][3:5]) * 60000
			ss=int(nsdata[i][4][6:8]) * 1000
			ms=int(nsdata[i][4][9:12])
			nsdata[i][4]=hh+mm+ss+ms
		except IndexError:
			pass
		except ValueError:
			pass
	return nsdata


def filter_nsevent(filtered_nslog,*event_tags):
	"""
	Syntax: filter_nsevent(cleaned data from previous function filter_nslog,'event_tags1','event_tags2'...)
	Example: filter_nsevent(nsdata,'int','ope','clo','gaz')

	This function takes in the resulted filtered data from previous function filter_nslog,
	and takes variable arguments with user specific event tags.
	Note that it reads the first three letters of the event tags as NetStation communication is limiting with 4 letters.
	"""
	filtered_nsevent=[]
	for event in event_tags:
		for i in range(0,len(filtered_nslog)):
			if filtered_nslog[i][0][0:3]==str(event):
				filtered_nsevent.append(filtered_nslog[i])
	# filtered_nsevent=filtered_nsevent.sort(key=lambda x: x[4])
	filtered_nsevent=sorted(filtered_nsevent, key=lambda x: int(x[4]))
	return filtered_nsevent


def timediff_ns(filtered_nsevent):
	"""
	Example: timediff_py(filtered_nsevent)

	This function takes in the sorted event list, and takes difference of every each item.
	Resulted time difference is in milliseconds.
	ie. item[1]-item[0], item[2]-item[1] ...
	"""
	diff_ns=[]
	for i in range(0,len(filtered_nsevent)-1):
		diff_ns.append(filtered_nsevent[i+1][4]-filtered_nsevent[i][4])
	return diff_ns


def average_diff(diff_py,diff_ns):
	"""
	Example: average_diff(diff_py,diff_ns)

	This function takes in two lists calculated from timediff_py and timediff_ns,
	compares each index between the two lists.
	Then calculates the absolute value, and returns averages.
	"""
	if len(diff_py) != len(diff_ns):
		print("Length of Py log and Ns log different. Make sure event tags match.")
		return
	else:
		diff=list(np.array(diff_py)-np.array(diff_ns))
		for i in range(0,len(diff)):
			diff[i]=round(diff[i],2)
			diff[i]=abs(diff[i])
			#give simple text warning if difference exceeds over 15ms
			if diff[i] >= 15:
				print("WARNING: big diff at PY-NS timing: index# " + str(i) + ": " + str(diff[i]) + " (above 15ms)")
	avg=round(sum(diff)/len(diff),2)
	return avg


### PsychoPy Photocell Timing ###
def photocell_py(filename, pc_tag, *event_tags):
	"""
	Syntax: photocell_py(string of filename w/o extension, 'photocell tag labeled as in Py log', 'custom event tags')
	Example: photocell_py('test2','wsq','ope','clo','gaz')

	This function takes in csv filename of PsychoPy log, and measures time difference of each
	photocell tag - previous event tag = photocell time delay
	"""
	filtered_pylog=filter_pylog(str(filename),'data')
	filtered_pc,diff_pypc=[],[]
	#filter pc_tag to list
	for i in range(0,len(filtered_pylog)):
		if filtered_pylog[i][2][0:3]==str(pc_tag):
			filtered_pc.append(filtered_pylog[i])
	#filter custom event_tags to list
	for event in event_tags:
		for i in range(0,len(filtered_pylog)):
			if filtered_pylog[i][2][0:3]==str(event):
				filtered_pc.append(filtered_pylog[i])
	filtered_pc=sorted(filtered_pc)
	#calculate photocell timing difference
	for i in range(0,len(filtered_pc)):
		if filtered_pc[i][2][0:3]==str(pc_tag):
			diff_pypc.append(round(float(filtered_pc[i][0])-float(filtered_pc[i-1][0]),3))

	#give simple text warning if difference exceeds over 15ms
	for i in range(0,len(diff_pypc)):
		if diff_pypc[i] >= 15:
			print("Warning: big diff at Py index# " + str(i) + ": " + str(diff_pypc[i]) + " (above 15ms)")
	if len(diff_pypc) != 0:
		avg_pypc=round(sum(diff_pypc)/len(diff_pypc),1)
	return avg_pypc


### NetStation Photocell Timing ###
def photocell_ns(filename, *event_tags):
	"""
	Syntax: photocell_ns(string of filename w/o extension, 'custom event tags')
	Example: photocell_py('test2','ope','clo','gaz')

	This function takes in csv filename of NetStation event log, and measures time difference of each
	photocell tag - previous event tag = photocell time delay

	***Note: unlike PsychoPy log, NetStation photocell label is fixed as DIN3 or DIN'X'
	Also, there is an extra DIN3 at the end, so the last one is not counted.
	"""
	filtered_pc,diff_nspc=[],[]
	din3_sort, din3_diff=[],[]
	nsdata=filter_nslog(str(filename))
	#append DIN3 labeled events
	for i in range(0,len(nsdata)-1):
		if (nsdata[i][0]=='DIN3'):
			filtered_pc.append(nsdata[i])
	#append custom event tags
	for event in event_tags:
		for i in range(0,len(nsdata)-1):
			if nsdata[i][0][0:3]==str(event):
				filtered_pc.append(nsdata[i])
	#sort list in time onset order
	filtered_pc=sorted(filtered_pc, key=lambda x: int(x[4]))
	#calculate photocell timing difference
	for i in range(0,len(filtered_pc)):
		if filtered_pc[i][0]=='DIN3':
			diff_nspc.append(filtered_pc[i][4]-filtered_pc[i-1][4])

	#give simple text warning if difference exceeds over 15ms
	for i in range(0, len(diff_nspc)):
		if diff_nspc[i] >= 15:
			print("WARNING: big diff at NS Photocell index# " + str(i) + ": " + str(diff_nspc[i]) + " (above 15ms)")
	if len(diff_nspc) != 0:
		avg_nspc=round(sum(diff_nspc)/len(diff_nspc),1)
	return avg_nspc
