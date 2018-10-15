"""
This file compiles all the functions from pyns_core.py into a single function
'pyns_run' allows to insert custom event labels as variable length argument
See function help for details of each argument ie. help(pyns_run)

Basic syntax:
Example1 = pyns_run('test2','test1','data','int','ope','clo','gaz','end')
Example2 = pyns_pc('test2','test1','wsq','ope','clo','gaz')
"""

from text_to_csv import text_to_csv
import pyns_core as pyns

def pyns_run(pylog, nslog, filter_py='data', *event_tags):
	"""
	Compiles all the functions from pyns_core.py to compare PsychoPy and NetStation logs.

	Example1 = pyns_run('test2','test1','data','int','ope','clo','gaz','end')

	**Args:
	pylog: 'filename' string of PsychoPy log
	nslog: 'filename' string of NetStation event log
	filter_py: string label that we want to filter out from PsychoPy log format
			   'data' should be used unless specific change in experiment code
	*event_tags: list all custom label tags in strings separated each by comma
	"""
	#convert log text files to readable csv files
	text_to_csv(str(nslog),str(pylog))

	#PsychoPy processing: filter_pylog -> filter_pyevent -> timediff_py
	filtered_pylog   = pyns.filter_pylog(str(pylog),str(filter_py))
	filtered_pyevent = pyns.filter_pyevent(filtered_pylog,*event_tags)
	diff_py          = pyns.timediff_py(filtered_pyevent)

	print('PsychoPy timing differences: ' + str(diff_py))

	#NetStation processing: filter_nslog -> filter_nsevent -> timediff_ns
	filtered_nslog   = pyns.filter_nslog(str(nslog))
	filtered_nsevent = pyns.filter_nsevent(filtered_nslog,*event_tags)
	diff_ns          = pyns.timediff_ns(filtered_nsevent)

	print('NetStation timing differences: ' + str(diff_ns))

	avg=pyns.average_diff(diff_py,diff_ns)
	print "Average Psychopy-Netstation: " + str(avg) + " ms"
	return avg

Example1 = pyns_run('test2','test1','data','int','ope','clo','gaz','end')


### Photocell Timing ###
def pyns_pc(pylog, nslog, pypc_tag='wsq', *event_tags):
	"""
	Compiles PsychoPy's and NetSTation's photocell functions and print out each timing
	Gives warning if timing difference is above 15 ms

	Example2 = pyns_pc('test2','test1','wsq','ope','clo','gaz')

	**Args:
	pylog: 'filename' string of PsychoPy log
	nslog: 'filename' string of NetStation event log
	pypc_tag: string label that's hardcoded in PsychoPy experiment code to mark 'photocell' event
		   'wsq' is used for basic run task
		   *event_tags: list all custom label tags in strings separated each by comma
	"""
	filtered_pypc    = pyns.photocell_py(str(pylog),pypc_tag,*event_tags)
	filtered_nspc    = pyns.photocell_ns(str(nslog),*event_tags)
	print('Average PsychoPy photocell timing diff: ' + str(filtered_pypc) + ' ms')
	print('Average NetStation photocell timing diff: ' + str(filtered_nspc) + ' ms')
	return filtered_pypc, filtered_nspc

Example2 = pyns_pc('test2','test1','wsq','ope','clo','gaz')
