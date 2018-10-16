#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This function runs simple basic tasks (ie. eye open & close, gaze) and photocell alignment
to properly configure lab environment prior to running the actual EEG.
Run this .py file on PsychoPy.

Below, You can set swtiches to change environment, or change variables to vary the duration of experiment.
Read commented descriptions for detail.

Ex. To run this locally on your device without NetStation connection, make sure to turn switches:
netstation=False
recording=False
"""
from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os
import sys
import decimal

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                       Custom Variables                          #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Switches #
netstation  = False       #False to run the file locally without connecting to NetStation
recording   = False       #True starts recording NetStation automatically
photocell   = True        #True allows use of photocell device
systemSound = True        #True is recommended // plays sound feedback to open your eyes

# Main task/routine durations in frames #
dur_description=240   #duration of instruction page
dur_open=300          #open/blinking eyes
dur_close=300         #eyes closed
dur_gazL=300          #gaze left
dur_gazR=300          #gaze right
dur_gazU=300          #gaze up
dur_gazD=300          #gaze down
gaze_pos=0.9          #cross position (proportional to screen)
                      #position will be L(-0.7,0),R(0.7,0) ... so on

# Photocell variables #Default values are based on current lab environment
dur_whitesquare=0.001 #Minimize duration of photocell square blinking
square_width=0.5      #default: 0.5 cm
square_height=0.5     #default: 0.5 cm
square_pos=(14.9,11.2)#default: (14.9,11.2)
square_opac=0.9       #default: 0.9 (range from 0-1)

# Misc #
frameRate_backup=60   #backup switch for framerate. Default = 60
dur_beepsound=1.5     #systemSound should be true

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                       Experiment Code                           #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# NetStation setup
if netstation:
    import egi.simple as egi
    ms_localtime = egi.ms_localtime
    ns = egi.Netstation()
    print("Imported PyNetstation")

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Experiment session info
expName = 'pyns_exp'
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1.0,-1.0,-1.0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / frameRate_backup

# Initialize components for white space for photocell to read
# width(x,y), height(x,y) = x is width, y is height in cm
if photocell:
    whitesquare = visual.Rect(
        win=win, name='whitesquare', units='cm',
        width=(square_width, square_height)[0], height=(square_width, square_height)[1],
        ori=0, pos=square_pos,
        lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
        fillColor=[1,1,1], fillColorSpace='rgb',
        opacity=square_opac, depth=0.0, interpolate=True)

    alignClock = core.Clock()
    align_text = visual.TextStim(win=win, name='intro_text',
    text='Align the photocell to the white space displayed on the screen. \n\nPress spacebar to proceed.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "intro"
introClock = core.Clock()
intro_text = visual.TextStim(win=win, name='intro_text',
    text='Welcome.\n\nYou will be instructed to perform basic tasks. Please follow the instructions carefully. \n\nPress spacebar to begin.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "open"
openClock = core.Clock()
open_text = visual.TextStim(win=win, name='open_text',
    text='Keep your eyes open while fixating on cross for %s seconds\n\n' %(round(dur_open/expInfo['frameRate'],0)),
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);
fixation = visual.TextStim(win=win, name='fixation',
    text='+\n',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

# Initialize components for Routine "close"
closeClock = core.Clock()
if systemSound:
    tmp_txt='Keep your eyes closed for ' + str(round(dur_close/expInfo['frameRate'],0)) + ' seconds. Open your eyes after a beep sound'
else:
    tmp_txt='Keep your eyes closed for ' + str(round(dur_close/expInfo['frameRate'],0)) + ' seconds and open your eyes'
close_text = visual.TextStim(win=win, name='close_text',
    text=tmp_txt,
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);
blank = visual.TextStim(win=win, name='blank',
    text=' ',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
if systemSound:
    beep = sound.Sound('A', secs=dur_beepsound)
    beep.setVolume(1)

# Initialize components for Routine "gaze"
gazeClock = core.Clock()
gaze_text = visual.TextStim(win=win, name='gaze_text',
    text='Fixate on the cross that appears on the screen\n',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);
left = visual.TextStim(win=win, name='left',
    text='+',
    font='Arial',
    pos=(-gaze_pos, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
right = visual.TextStim(win=win, name='right',
    text='+\n',
    font='Arial',
    pos=(gaze_pos, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0);
up = visual.TextStim(win=win, name='up',
    text='+',
    font='Arial',
    pos=(0, gaze_pos), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0);
down = visual.TextStim(win=win, name='down',
    text='+',
    font='Arial',
    pos=(0, -gaze_pos), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-4.0);

# Initialize components for Routine "end"
endClock = core.Clock()
esc = visual.TextStim(win=win, name='esc',
    text="End of test\n\nPress 'esc'",
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# ------Prepare to start Routine "align"-------
if photocell:
    t = 0
    alignClock.reset()
    frameN = -1
    continueRoutine = True
# update component parameters for each repeat
    next = event.BuilderKeyResponse()
# keep track of which components have finished
    alignComponents = [align_text, next]
    for thisComponent in alignComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
if not photocell:
    continueRoutine = False
    align_text = ''
# update component parameters for each repeat
    next = event.BuilderKeyResponse()
# keep track of which components have finished
    alignComponents = [align_text, next]

# -------Start Routine "align"-------
while continueRoutine and photocell:
    # get current time
    t = alignClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *align_text* updates
    if frameN >= 0.0 and align_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        align_text.tStart = t
        align_text.frameNStart = frameN  # exact frame index
        align_text.setAutoDraw(True)
        whitesquare.setAutoDraw(True)

    # *next* updates
    if frameN >= 0.0 and next.status == NOT_STARTED:
        # keep track of start time/frame for later
        next.tStart = t
        next.frameNStart = frameN  # exact frame index
        next.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(next.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if next.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            next.keys = theseKeys[-1]  # just the last key pressed
            next.rt = next.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in alignComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "align"-------
for thisComponent in alignComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
        whitesquare.setAutoDraw(False)
# check responses
if next.keys in ['', [], None]:  # No response was made
    next.keys=None
thisExp.addData('next.keys',next.keys)
if next.keys != None:  # we had a response
    thisExp.addData('next.rt', next.rt)
thisExp.nextEntry()
# the Routine "intro" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()


# ------Prepare to start Routine "intro"-------
t = 0
introClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
next = event.BuilderKeyResponse()
# keep track of which components have finished
introComponents = [intro_text, next]
for thisComponent in introComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# NetStation
if netstation:
    ns.connect('10.0.0.42', 55513)
    ns.BeginSession()
    print("Connected to Netstation")
    if recording:
        ns.StartRecording()
        print("Recording ...")

# -------Start Routine "intro"-------

### NetStation ###
if netstation:
    ns.sync()
    logging.data('intS' + ' | total frame duration: ' + str(frameN))
    ns.send_event(key='intS', timestamp=None,pad=False)

while continueRoutine:
    # get current time
    t = introClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *intro_text* updates
    if frameN >= 0.0 and intro_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        intro_text.tStart = t
        intro_text.frameNStart = frameN  # exact frame index
        intro_text.setAutoDraw(True)

    # *next* updates
    if frameN >= 0.0 and next.status == NOT_STARTED:
        # keep track of start time/frame for later
        next.tStart = t
        next.frameNStart = frameN  # exact frame index
        next.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(next.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if next.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            next.keys = theseKeys[-1]  # just the last key pressed
            next.rt = next.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in introComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "intro"-------
for thisComponent in introComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if next.keys in ['', [], None]:  # No response was made
    next.keys=None
thisExp.addData('next.keys',next.keys)
if next.keys != None:  # we had a response
    thisExp.addData('next.rt', next.rt)
thisExp.nextEntry()
# the Routine "intro" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

### NetStation ###
if netstation:
    ns.sync()
    logging.data('intE' + ' | total frame duration: ' + str(frameN))
    ns.send_event(key='intE', timestamp=None,pad=False)

# ------Prepare to start Routine "open"-------
t = 0
openClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
openComponents = [open_text, fixation]
for thisComponent in openComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "open"-------
while continueRoutine:
    # get current time
    t = openClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *open_text* updates
    if t >= 0.0 and open_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        open_text.tStart = t
        open_text.frameNStart = frameN  # exact frame index
        open_text.setAutoDraw(True)
    if open_text.status == STARTED and frameN >= (open_text.frameNStart + dur_description):
        open_text.setAutoDraw(False)

    # *fixation* updates
    if frameN >= dur_description and fixation.status == NOT_STARTED:
        ### NetStation ###
        if netstation:
            ns.sync()
            logging.data('opeS' + ' | total frame duration: ' + str(frameN))
            ns.send_event(key='opeS', timestamp=None,pad=False)

        # keep track of start time/frame for later
        fixation.tStart = t
        fixation.frameNStart = frameN  # exact frame index
        fixation.setAutoDraw(True)
        if photocell:
            whitesquare.setAutoDraw(True)
            logging.data('wsqS')
    if photocell and (frameN >= dur_description+dur_whitesquare):
        whitesquare.setAutoDraw(False)

    if fixation.status == STARTED and frameN >= (fixation.frameNStart + dur_open):
        fixation.setAutoDraw(False)

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in openComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "open"-------
for thisComponent in openComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "open" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

### NetStation ###
if netstation:
    ns.sync()
    logging.data('opeE' + ' | total frame duration: ' + str(frameN))
    ns.send_event(key='opeE', timestamp=None,pad=False)

# ------Prepare to start Routine "close"-------
t = 0
closeClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
if systemSound:
    beep.setSound('A', secs=5)
# keep track of which components have finished
if systemSound:
    closeComponents = [close_text, blank, beep]
else:
    closeComponents = [close_text, blank]

for thisComponent in closeComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "close"-------
while continueRoutine:
    # get current time
    t = closeClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *close_text* updates
    if frameN >= 0.0 and close_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        close_text.tStart = t
        close_text.frameNStart = frameN  # exact frame index
        close_text.setAutoDraw(True)
    if close_text.status == STARTED and frameN >= (close_text.frameNStart + dur_description):
        close_text.setAutoDraw(False)

    # *blank* updates
    if frameN >= dur_description and blank.status == NOT_STARTED:
        ### NetStation ###
        if netstation:
            ns.sync()
            logging.data('cloS' + ' | total frame duration: ' + str(frameN))
            ns.send_event(key='cloS', timestamp=None,pad=False)

        # keep track of start time/frame for later
        blank.tStart = t
        blank.frameNStart = frameN  # exact frame index
        blank.setAutoDraw(True)
        if photocell:
            whitesquare.setAutoDraw(True)
            logging.data('wsqS')
    if photocell and (frameN >= dur_description+dur_whitesquare):
        whitesquare.setAutoDraw(False)
    if blank.status == STARTED and frameN >= (blank.frameNStart + dur_close):
        blank.setAutoDraw(False)
    # start/stop beep
    if systemSound:
        if frameN >= (dur_description+dur_close) and beep.status == NOT_STARTED:
            ### NetStation ###
            if netstation:
                ns.sync()
                logging.data('beep' + ' | total frame duration: ' + str(frameN))
                ns.send_event(key='beep', timestamp=None,pad=False)

            # keep track of start time/frame for later
            beep.tStart = t
            beep.frameNStart = frameN  # exact frame index
            beep.play()  # start the sound (it finishes automatically)
            core.wait(dur_beepsound)
            beep.stop()
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in closeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "close"-------
for thisComponent in closeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "close" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

### NetStation ###
if netstation:
    ns.sync()
    logging.data('cloE' + ' | total frame duration: ' + str(frameN))
    ns.send_event(key='cloE', timestamp=None,pad=False)

# ------Prepare to start Routine "gaze"-------
t = 0
gazeClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
gazeComponents = [gaze_text, left, right, up, down]
for thisComponent in gazeComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "gaze"-------

while continueRoutine:
    # get current time
    t = gazeClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *gaze_text* updates
    if frameN >= 0.0 and gaze_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        gaze_text.tStart = t
        gaze_text.frameNStart = frameN  # exact frame index
        gaze_text.setAutoDraw(True)
    if gaze_text.status == STARTED and frameN >= (gaze_text.frameNStart + dur_description):
        gaze_text.setAutoDraw(False)

    # *left* updates
    if frameN >= dur_description and left.status == NOT_STARTED:
        ### NetStation ###
        if netstation:
            ns.sync()
            logging.data('gazL' + ' | total frame duration: ' + str(frameN))
            ns.send_event(key='gazL', timestamp=None,pad=False)

        # keep track of start time/frame for later
        left.tStart = t
        left.frameNStart = frameN  # exact frame index
        left.setAutoDraw(True)
        if photocell:
            whitesquare.setAutoDraw(True)
            logging.data('wsqS')
    if photocell and (frameN >= dur_description+dur_whitesquare):
        whitesquare.setAutoDraw(False)
    if left.status == STARTED and frameN >= (left.frameNStart + dur_gazL):
        left.setAutoDraw(False)

    # *right* updates
    if frameN >= (dur_description+dur_gazL) and right.status == NOT_STARTED:
        ### NetStation ###
        if netstation:
            ns.sync()
            logging.data('gazR' + ' | total frame duration: ' + str(frameN))
            ns.send_event(key='gazR', timestamp=None,pad=False)

        # keep track of start time/frame for later
        right.tStart = t
        right.frameNStart = frameN  # exact frame index
        right.setAutoDraw(True)
        if photocell:
            whitesquare.setAutoDraw(True)
            logging.data('wsqS')
    if photocell and (frameN >= dur_description+dur_gazL+dur_whitesquare):
        whitesquare.setAutoDraw(False)
    if right.status == STARTED and frameN >= (right.frameNStart + dur_gazR):
        right.setAutoDraw(False)

    # *up* updates
    if frameN >= (dur_description+dur_gazL+dur_gazR) and up.status == NOT_STARTED:
        ### NetStation ###
        if netstation:
            ns.sync()
            logging.data('gazU' + ' | total frame duration: ' + str(frameN))
            ns.send_event(key='gazU', timestamp=None,pad=False)

        # keep track of start time/frame for later
        up.tStart = t
        up.frameNStart = frameN  # exact frame index
        up.setAutoDraw(True)
        if photocell:
            whitesquare.setAutoDraw(True)
            logging.data('wsqS')
    if photocell and (frameN >= dur_description+dur_gazL+dur_gazR+dur_whitesquare):
        whitesquare.setAutoDraw(False)
    if up.status == STARTED and frameN >= (up.frameNStart + dur_gazU):
        up.setAutoDraw(False)

    # *down* updates
    if frameN >= (dur_description+dur_gazL+dur_gazR+dur_gazU) and down.status == NOT_STARTED:
        ### NetStation ###
        if netstation:
            ns.sync()
            logging.data('gazD' + ' | total frame duration: ' + str(frameN))
            ns.send_event(key='gazD', timestamp=None,pad=False)

        # keep track of start time/frame for later
        down.tStart = t
        down.frameNStart = frameN  # exact frame index
        down.setAutoDraw(True)
        if photocell:
            whitesquare.setAutoDraw(True)
            logging.data('wsqS')
    if photocell and (frameN >= dur_description+dur_gazL+dur_gazR+dur_gazD+dur_whitesquare):
        whitesquare.setAutoDraw(False)
    if down.status == STARTED and frameN >= (down.frameNStart + dur_gazD):
        down.setAutoDraw(False)

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in gazeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "gaze"-------
for thisComponent in gazeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "gaze" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# NetStation
if netstation:
    ns.sync()
    logging.data('gazE' + ' | total frame duration: ' + str(frameN))
    ns.send_event(key='gazE', timestamp=None,pad=False)

# ------Prepare to start Routine "end"-------
t = 0
endClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
endComponents = [esc]
for thisComponent in endComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "end"-------
while continueRoutine:
    # get current time
    t = endClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *esc* updates
    if t >= 0.0 and esc.status == NOT_STARTED:
        # keep track of start time/frame for later
        esc.tStart = t
        esc.frameNStart = frameN  # exact frame index
        esc.setAutoDraw(True)
    if esc.status == STARTED and frameN >= (esc.frameNStart + 60):
        esc.setAutoDraw(False)

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# NetStation
if netstation:
    ns.sync()
    logging.data('endE' + ' | total frame duration: ' + str(frameN))
    ns.send_event(key='endE', timestamp=None,pad=False)

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
