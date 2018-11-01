#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This function runs simple basic tasks (ie. eye open & close, blink, gaze) and photocell alignment
to properly configure EEG environment prior to running the actual experiment.
Run this .py file on PsychoPy.

Below, You can set swtiches and change variables to vary the duration of experiment.
Read comments for detail.

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
# 1=blinks
# 2=open/close
# 3=gaze
seq=[1,1,1,1,2,2,2,3,3]
shuffle(seq)
# Switches #
netstation  = False       #False to run the file locally without connecting to NetStation
recording   = False       #True starts recording NetStation automatically
photocell   = True        #True allows use of photocell device

# Duration of blank transition
dur_iti=10
# 'blink' custom var:
blink_per_block=4
blink_isi=120
# 'openclose' custom var:
openclose_per_block=2
openclose_isi=120
# 'gaze' custom var:
gaze_per_block=2     #1=look left, right, up, down one each
gaze_isi=90

# Cross size/position
cross_size=0.5
gaze_horizontal_pos=13        #cross position in cm
gaze_vertical_pos=10          #cross position in cm
# Photocell variables #Default values are based on current lab environment
dur_whitesquare=1 #Minimize duration of photocell square blinking
square_width=0.5      #default: 0.5 cm
square_height=0.5     #default: 0.5 cm
square_pos=(14.9,11.2)#default: (14.9,11.2)
square_opac=0.9       #default: 0.9 (range from 0-1)

# Durations ! Do not change!
dur_blink = (blink_per_block+1)*blink_isi+(blink_per_block*60)+dur_iti
oc_seq=[1,2]*openclose_per_block
dur_openclose = (len(oc_seq)+1)*openclose_isi+(len(oc_seq)*60)+dur_iti
temp = ['']
gaze_seq=['l','r','u','d']*gaze_per_block
shuffle(gaze_seq)
gaze_seq=temp+gaze_seq
dur_gaze= (len(gaze_seq)+1)*gaze_isi+(len(gaze_seq)*60)+dur_iti


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                    Initialize Components                        #
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

win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1.0,-1.0,-1.0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
expInfo['frameRate'] = win.getActualFrameRate()

# Prepare components
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

introClock = core.Clock()
openClock = core.Clock()
closeClock = core.Clock()
gazeClock = core.Clock()
endClock = core.Clock()

intro_text = visual.TextStim(win=win, name='intro_text',
    text='Hello,\n\nA sound will be played, instructing what to do. \nYou will be told to OPEN/CLOSE eyes, BLINK, or LOOK at specific direction. When looking at specific direction, make sure you look and fixate back to the center.\n\nPress spacebar to begin.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);
center = visual.ShapeStim(win=win, name='center', units='cm',vertices='cross',
    size=(cross_size, cross_size),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
left = visual.ShapeStim(win=win, name='left', units='cm',vertices='cross',
    size=(cross_size, cross_size),
    ori=0, pos=(-gaze_horizontal_pos, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
right = visual.ShapeStim(win=win, name='right', units='cm',vertices='cross',
    size=(cross_size, cross_size),
    ori=0, pos=(gaze_horizontal_pos, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
up = visual.ShapeStim(win=win, name='up', units='cm',vertices='cross',
    size=(cross_size, cross_size),
    ori=0, pos=(0, gaze_vertical_pos),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
down = visual.ShapeStim(win=win, name='down', units='cm',vertices='cross',
    size=(cross_size, cross_size),
    ori=0, pos=(0, -gaze_vertical_pos),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
blank = visual.TextStim(win=win, name='blank',
    text=' ',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

# Sound Set
sclo = sound.Sound('./sound/close_speak.wav')
sclo.setVolume(1)
sope = sound.Sound('./sound/open_speak.wav')
sope.setVolume(1)
sbli = sound.Sound('./sound/blink_speak.wav')
sbli.setVolume(1)
slef = sound.Sound('./sound/left_speak.wav')
slef.setVolume(1)
srig = sound.Sound('./sound/right_speak.wav')
srig.setVolume(1)
s_up = sound.Sound('./sound/up_speak.wav')
s_up.setVolume(1)
sdow = sound.Sound('./sound/down_speak.wav')
sdow.setVolume(1)

esc = visual.TextStim(win=win, name='esc',
    text="End of test\n\nPress 'esc'",
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# helper functions:
def show_screen():
    center.setAutoDraw(True)
    left.setAutoDraw(True)
    right.setAutoDraw(True)
    up.setAutoDraw(True)
    down.setAutoDraw(True)
def hide_screen():
    center.setAutoDraw(False)
    left.setAutoDraw(False)
    right.setAutoDraw(False)
    up.setAutoDraw(False)
    down.setAutoDraw(False)

# ------Prepare to start Routine "align"-------
if photocell:
    t = 0
    alignClock.reset()
    frameN = -1
    continueRoutine = True
    next = event.BuilderKeyResponse()
    alignComponents = [align_text, next]
    for thisComponent in alignComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
if not photocell:
    continueRoutine = False
    align_text = ''
    next = event.BuilderKeyResponse()
    alignComponents = [align_text, next]
# -------Start Routine "align"-------
while continueRoutine and photocell:
    t = alignClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    if frameN >= 0.0 and align_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        align_text.tStart = t
        align_text.frameNStart = frameN  # exact frame index
        align_text.setAutoDraw(True)
        whitesquare.setAutoDraw(True)
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
    logging.data('intS' + ' | frame count: ' + str(frameN))
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
    logging.data('intE' + ' | frame count: ' + str(frameN))
    ns.send_event(key='intE', timestamp=None,pad=False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                       Experiment Loop                           #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
for trial in range(len(seq)):
    # check for blinks
    if seq[trial] == 1:
        t = 0
        openClock.reset()
        frameN = -1
        sclo.setSound('./sound/blink_speak.wav')
        blink_interval=[]
        pc_start=[]
        pc_end=[]

        if netstation:
            ns.sync()
            logging.data('bliS' + ' | frame count: ' + str(frameN))
            ns.send_event(key='bliS', timestamp=None,pad=False)

        for frameN in range(dur_blink):
            t = openClock.getTime()
            frameN = frameN + 1
            win.flip()
            show_screen()

            for i in range(blink_per_block+1):
                if frameN == blink_isi * i + (60 * (i-1)):
                    sbli.play()
                    if netstation:
                        ns.sync()
                        logging.data('sbli' + ' | frame count: ' + str(frameN))
                        ns.send_event(key='sbli', timestamp=None,pad=False)
                    blink_interval.append(frameN)
                    pc_start=[x+20 for x in blink_interval]
                    pc_end=[x+dur_whitesquare for x in pc_start]
            if photocell:
                for i in range(len(pc_start)):
                    if frameN == pc_start[i]:
                        whitesquare.setAutoDraw(True)
                        logging.data('wsqS')
                for i in range(len(pc_end)):
                    if frameN == pc_end[i]:
                        whitesquare.setAutoDraw(False)
            if dur_blink-frameN < dur_iti:
                hide_screen()

        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        routineTimer.reset()
        if netstation:
            ns.sync()
            logging.data('bliE' + ' | frame count: ' + str(frameN))
            ns.send_event(key='bliE', timestamp=None,pad=False)

    # check for open/close
    if seq[trial] == 2:
        t = 0
        closeClock.reset()
        frameN = -1
        sclo.setSound('./sound/close_speak.wav')
        sope.setSound('./sound/open_speak.wav')
        oc_interval=[]
        pc_start=[]
        pc_end=[]

        if netstation:
            ns.sync()
            logging.data('oc_S' + ' | frame count: ' + str(frameN))
            ns.send_event(key='oc_S', timestamp=None,pad=False)

        for frameN in range(dur_openclose):
            t = closeClock.getTime()
            frameN = frameN + 1
            win.flip()
            show_screen()

            for i in range(1,len(oc_seq)+1):
                if frameN == openclose_isi * i + (60 * (i - 1)):
                    if i % 2 != 0: # check for odd seq
                        sclo.play()
                        if netstation:
                            ns.sync()
                            logging.data('sclo' + ' | frame count: ' + str(frameN))
                            ns.send_event(key='sclo', timestamp=None,pad=False)
                    if i % 2 == 0: # check for even seq
                        sope.play()
                        if netstation:
                            ns.sync()
                            logging.data('sope' + ' | frame count: ' + str(frameN))
                            ns.send_event(key='sope', timestamp=None,pad=False)
                    oc_interval.append(frameN)
                    pc_start=[x+30 for x in oc_interval]
                    pc_end=[x+dur_whitesquare for x in pc_start]
            if photocell:
                for i in range(len(pc_start)):
                    if frameN == pc_start[i]:
                        whitesquare.setAutoDraw(True)
                        logging.data('wsqS')
                for i in range(len(pc_end)):
                    if frameN == pc_end[i]:
                        whitesquare.setAutoDraw(False)
            if dur_openclose-frameN < dur_iti:
                hide_screen()

        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        routineTimer.reset()
        if netstation:
            ns.sync()
            logging.data('oc_E' + ' | frame count: ' + str(frameN))
            ns.send_event(key='oc_E', timestamp=None,pad=False)


    # check for gaze
    if seq[trial] == 3:
        t = 0
        gazeClock.reset()
        frameN = -1
        slef.setSound('./sound/left_speak.wav')
        srig.setSound('./sound/right_speak.wav')
        s_up.setSound('./sound/up_speak.wav')
        sdow.setSound('./sound/down_speak.wav')
        gaze_interval=[]
        pc_start=[]
        pc_end=[]

        if netstation:
            ns.sync()
            logging.data('gazS' + ' | frame count: ' + str(frameN))
            ns.send_event(key='gazS', timestamp=None,pad=False)

        for frameN in range(dur_gaze):
            t = gazeClock.getTime()
            frameN = frameN + 1
            win.flip()
            show_screen()
            for i in range(1,len(gaze_seq)):
                if frameN == gaze_isi * i + (60 * (i - 1)):
                    if gaze_seq[i]=='l':
                        slef.play()
                        if netstation:
                            ns.sync()
                            logging.data('slef')
                            ns.send_event(key='slef', timestamp=None,pad=False)
                    if gaze_seq[i]=='r':
                        srig.play()
                        if netstation:
                            ns.sync()
                            logging.data('srig')
                            ns.send_event(key='srig', timestamp=None,pad=False)
                    if gaze_seq[i]=='u':
                        s_up.play()
                        if netstation:
                            ns.sync()
                            logging.data('s_up')
                            ns.send_event(key='s_up', timestamp=None,pad=False)
                    if gaze_seq[i]=='d':
                        sdow.play()
                        if netstation:
                            ns.sync()
                            logging.data('sdow')
                            ns.send_event(key='sdow', timestamp=None,pad=False)
                    gaze_interval.append(frameN)
                    pc_start=[x+20 for x in gaze_interval]
                    pc_end=[x+dur_whitesquare for x in pc_start]
            if photocell:
                for i in range(len(pc_start)):
                    if frameN == pc_start[i]:
                        whitesquare.setAutoDraw(True)
                        logging.data('wsqS')
                for i in range(len(pc_end)):
                    if frameN == pc_end[i]:
                        whitesquare.setAutoDraw(False)
            if dur_gaze-frameN < dur_iti:
                hide_screen()

        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        routineTimer.reset()
        if netstation:
            ns.sync()
            logging.data('gazE' + ' | frame count: ' + str(frameN))
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
    logging.data('endE' + ' | frame count: ' + str(frameN))
    ns.send_event(key='endE', timestamp=None,pad=False)

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
