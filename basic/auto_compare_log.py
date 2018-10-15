###########################################################
###   Converts tab-deliminated event text file to csv   ###
########################################################### 
import csv
import time
import pandas as pd 
import numpy as np
import math

nslog=[]
pplog=[]
ppdiff=[]
nsdiff=[]

#open csv files for 1.Netstation event log 2.PsyhoPy timing
with open('test.csv') as csvDataFile:
	data=list(csv.reader(csvDataFile))

with open('autolog.csv') as csvDataFile2:
	data2=list(csv.reader(csvDataFile2))

##cleaning data/gets 'Onset' from the text file
for i in range(0,len(data)):
	if data[i][0]=='auto':
		nslog.append(data[i][4])
	else:
		pass 
#removes '_' character in the items 
nslog=[i[1:] for i in nslog]

for i in range(0,len(data2)):
	data2[i]=data2[i][0]
data2=map(int,data2)
pplog=data2

#convert from string of HH:MM:SS:MMM to MS
for i in range(0,len(nslog)):
	hh=int(nslog[i][0:2]) * 3600000
	mm=int(nslog[i][3:5]) * 60000
	ss=int(nslog[i][6:8]) * 1000
	mmm=int(nslog[i][9:12])
	nslog[i]=hh+mm+ss+mmm

#calculate difference
for i in range(0,len(pplog)-1):
	ppdiff.append(pplog[i+1]-pplog[i])
for i in range(0,len(nslog)-1):
	nsdiff.append(nslog[i+1]-nslog[i])

diff=list(np.array(nsdiff)-np.array(ppdiff))
avg=sum(diff)/len(diff)
print diff, avg

# import numpy as np
# np.savetxt('filename.csv',varname,delimiter=',',fmt='%d')