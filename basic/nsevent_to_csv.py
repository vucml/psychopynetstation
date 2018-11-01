###########################################################
###   Converts tab-deliminated event text file to csv   ###
###########################################################
import csv
"""
USE: nsevent_to_csv('NS log name') to convert"
"""
##creates csv file identical to filename

def nsevent_to_csv(filenameA):
#convert NetStation event log txt file to csv
	txt_file = str(filenameA) #check extension
	csv_file = str(filenameA) + ".csv"

	in_txt = csv.reader(open(txt_file, "rb"), delimiter = '\t')
	out_csv = csv.writer(open(csv_file, 'wb'))

	out_csv.writerows(in_txt)
