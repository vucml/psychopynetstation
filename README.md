# PsychoPyNetStation (PyNs) 

**PsychoPyNetStation** provides basic experiment and data processing scripts that can be run prior to running the actual EEG experiments. The scripts help configure basic lab setups, such as photocell device and digital input connection, test for connectivity, and measure timing diffrence. With the data logs resulted from the experiment script (pyns_exp.py), pyns_run.py first cleans data. Then, it measures the relative timing difference between PsychoPy and NetStation by comparing the timestamps of stimuli onset in PsychoPy and event labels in NetStation. 

For full documentation and details, please refer to Wiki, or docstring of each function (ie. help(function name)). The default values and setup are all currently configured to lab environment. The experiment can be run on local device without NetStation connection as well.


## Prerequisites
All the codes are written in Python, and have been tested on PsychoPy 1.90.3. 

**For running experiment script: pyns_exp.py...**
1. It is recommended to have a **standlone PsychoPy** installed on the device. The lab currently uses PsychoPy 1.90.3 ([Link to PsychoPy GitHub](https://github.com/psychopy/psychopy/releases), which is the latest stable version. For instructions on installing PsychoPy, refer to Wiki page.
2. **egi pynetstation module**: even though this module comes with full standalone PsychoPy version, you can download it at [http://www.psychopy.org/api/hardware/egi.html](http://www.psychopy.org/api/hardware/egi.html). If you run the experiment code locally without NetStation connection, this module is not needed. 

**For running post-experiment script: pyns_run.py...** 
All the scripts are written in Python. Specifically, scripts import [csv](https://docs.python.org/2/library/csv.html), time, [numpy](https://www.scipy.org/scipylib/download.html), [pandas](https://pandas.pydata.org/), Decimal. If you do not have any one of the packages, you should download them regardless of running this experiment code as they are essential when programming with Python. 


## Getting Started
\*\* Refer to Wiki page for proper setup/running thoroughly
This section will quickly run through testing the experiment without NetStation connection. Then, using example files 'test1' (NetStation event text log) and 'test2' (PsychoPy experiment log), we will run process scripts to read timing difference. Throughout documentation and function docstrings, you may find 'test1' and 'test2' referred for this reason. 

### Part A: Running Experiment (pyns_exp.py)

1. Clone the repository to your local device. In terminal, navigate to whichever directory you want to download. Then: 
``` 
git clone https://github.com/vucml/PsychoPyNetStation.git
``` 

2. Open pyns_exp.py by opening or dragging it to PsychoPy. It should open the script in PsychoPy's Coder view. Look at section `Custom Variables` to change accordingly. You may also alter duration (in frames) below. 

  * Running without NetStation connection: 
```python
# Switches #
netstation  = False       #False to run the file locally without connecting to NetStation
recording   = False       #True starts recording NetStation automatically
``` 
  * Running with NetStation connection: 
```python
# Switches #
netstation  = True       #False to run the file locally without connecting to NetStation
recording   = False       #True starts recording NetStation automatically
```

  * Trouble-shooting/configuring sound or DIN input: You can vary the switches `photocell` and `systemSound`

3. Complete the experiment. The experiment will go through basic tasks, such as staring at the center cross, closing eyes, gazing (staring) at varing positions of cross. With NetStation connected, these would be helpful indicator/baseline for EEG waveforms. 

4. Once complete, experiment data will be saved in data file. The file extension with .log will be what we will be using for checking timing. 

### Part B: Running Post Experiment (pyns_run.py)

This section uses example files 'test1' and 'test2'. By the time you completed Part A with proper NetStation connection, you should have two log files: One from PsychoPy log and the other from NetStation event log. 

1. Run the following line in terminal. Make sure you are in the cloned directory. 
``` 
python -i pyns_run.py 
``` 

2. Upon entering Python, it will print some brief notes on usage. Now type: 
```python
example1 = pyns_diff('test2','test1','data','int','ope','clo','gaz','end')
``` 
This will print out the calculated average timing difference between event timestamps of PsychoPy and NetStation. You should get `5.89 ms`.

* If you had photocell connected, there is also `pyns_pc`: 
 ```python
example2 = pyns_pc('test2','test1','wsq','ope','clo','gaz')
``` 
This will print out average Photocell timing difference in PsychoPy and NetStation seperately. You should get `3.1` and `43.0` ms each. 


## Issues

Feel free to submit bugs/potential improvements on Issues :) 


## Acknowledgments

* pyns_exp base code is from PsychoPy builder
* EGI Pynetstation module is used for PsychoPy to EGI NetStation connection 

