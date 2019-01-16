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

# more advanced event send
def send_to_NS(code, trialnum, item, cond, category):
    """
    helper function to send signals with desired event tags, labels, cond for segmentation

    code = trial info ie. t1, t2, t3 ...
    label = 4 letter code sent to NS
    trialnum = t
    item = s                | item index number (1-27)
    cond = [1, 2, 3]        | fixation, light, heavy distraction
    category = [1, 2, 3]    | 1 = celeb, 2 = location, 3 = objects
    """
    if not practiceTrial and netstation:
        temp = 't' + str(trialnum)
        ns.sync()
        logging.data('trial ' + str(trialnum) + ' | ' + str(code) + ' | cond: ' + str(cond) + ' | cat: ' + str(category))
        ns.send_event(key=temp, label=str(code), timestamp=None, table={'item': item, 'cond': cond, 'catg': category}, pad=False)
