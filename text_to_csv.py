###########################################################
###   Converts tab-deliminated event text file to csv   ###
###########################################################
import csv
"""
USE: text_to_csv('NS log name', 'PsychoPy log name') to convert"
"""
##change filename & filename2 accordingly
##creates csv file identical to filename

def text_to_csv(filenameA, filenameB):
#convert NetStation event log txt file to csv
	txt_file = str(filenameA) #check extension
	csv_file = str(filenameA) + ".csv"

	in_txt = csv.reader(open(txt_file, "rb"), delimiter = '\t')
	out_csv = csv.writer(open(csv_file, 'wb'))

	out_csv.writerows(in_txt)

#convert PsychoPy log file to csv
	txt_file = str(filenameB) + ".log" #check extension
	csv_file = str(filenameB) + ".csv"

	in_txt = csv.reader(open(txt_file, "rb"), delimiter = '\t')
	out_csv = csv.writer(open(csv_file, 'wb'))

	out_csv.writerows(in_txt)
