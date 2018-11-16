# psychopynetstation (pyns)

**psychopynetstation** provides `pyns_exp.py` basic task scripts to test communication between PsychoPy and EGI NetStation, which is an EEG scanning software. `pyns_run.py` uses the resulted log files from PsychoPy and NetStation to measure stimuli timing difference. The code uses [PyNetStation](http://psychopy.org/api/hardware/egi.html) to send signals from PsychoPy to NetStation.

As the resources related to PsychoPy and NetStation connection seem very limiting, I tried compiling the materials learnt into organized [psychopynetstation wiki page](https://github.com/vucml/psychopynetstation/wiki). The wiki page has thorough details from installing PsychoPy, and laying out hardware to configuring NetStation software, managing and applying cap sensors to subjects.

For full documentation and details, please refer to Wiki, or docstring of each function (ie. help(function name)). The default values and setup are all currently configured to lab environment. The experiment can be run on local device without NetStation connection as well.

## Wiki table of content:

* [Home](https://github.com/vucml/psychopynetstation/wiki)
* [PsychoPy Setup](https://github.com/vucml/psychopynetstation/wiki/PsychoPy_Setup)
   * [Installing PsychoPy](https://github.com/vucml/psychopynetstation/wiki/Installing_PsychoPy1.90.3)
   * [Installing PyNetStation](https://github.com/vucml/psychopynetstation/wiki/Installing_PyNetStation)
* [Hardware Setup](https://github.com/vucml/psychopynetstation/wiki/Hardware_Setup)
* [NetStation Setup](https://github.com/vucml/psychopynetstation/wiki/NetStation_Setup)

* [Basic Tests](https://github.com/vucml/psychopynetstation/wiki/Basic_Tests)
   * [Sending Events & Timing Check](https://github.com/vucml/psychopynetstation/wiki/Sending_Events_and_Timing_Check)
   * [Photocell & DIN](https://github.com/vucml/psychopynetstation/wiki/Photocell_and_DIN)
   * [Full Basic EEG](https://github.com/vucml/psychopynetstation/wiki/Full_Basic_EEG)
   * [PyNetStation Code Summary](https://github.com/vucml/psychopynetstation/wiki/PyNetStation_Code_Summary)

* [Running EEG](https://github.com/vucml/psychopynetstation/wiki/Running_EEG)
   * [Preparation](https://github.com/vucml/psychopynetstation/wiki/Preparation)
   * [NetStation & Impedance Check](https://github.com/vucml/psychopynetstation/wiki/NetStation_and_Impedance_Check)
   * [Removing & Disinfecting](https://github.com/vucml/psychopynetstation/wiki/Removing_and_Disinfecting)
* [ERP Derivation](https://github.com/vucml/psychopynetstation/wiki/ERP_Derivation)
* [NetStation Manuals](https://github.com/vucml/psychopynetstation/wiki/NetStation_Manuals)
* [Trouble Shooting](https://github.com/vucml/psychopynetstation/wiki/Trouble_Shooting)


## Issues

Feel free to submit bugs/suggestions on Issues :)


## Acknowledgments

* pyns_exp's base code is based on PsychoPy builder and later changed
* EGI Pynetstation module is used for PsychoPy to EGI NetStation connection
