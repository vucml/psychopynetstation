#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This code simply checks whether photocell is working.
Place photocell roughly at the center of the screen, and run the file.
It will repeat 5 times showing white rectangles.
As white rectangles appear, you should see the DIN3 event being sent to NetStation.
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os
import sys

#########################################################################
#                            Custom Vars                                #
#########################################################################
nreps=5 # repetition to display white rectangle
frame_rate_manual=60 # default display 60Hz
dur_square=120
dur_blank=60
#########################################################################

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

expName = 'pyns_photocell'
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=[], runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True)
endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Setup the Window
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1.0,-1.0,-1.0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

# Setup frame rate
frame_rate=win.getActualFrameRate()
if frame_rate != None:
    frameDur=1.0/frame_rate
else:
    frameDur=1.0/frame_rate_manual

trialClock = core.Clock()
square = visual.Rect(
    win=win, name='square',
    width=(1.3, 1.3)[0], height=(1.3, 1.3)[1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
text = visual.TextStim(win=win, name='text',
    text=' ',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=5, method='random',
    extraInfo=[], originPath=-1,
    trialList=[None],
    seed=None, name='trials')
thisExp.addLoop(trials)
thisTrial = trials.trialList[0]
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:
    currentLoop = trials
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))

    # ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    trialComponents = [square, text]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

        # *square* updates
        if frameN >= dur_blank/2 and square.status == NOT_STARTED:
            # keep track of start time/frame for later
            square.tStart = t
            square.frameNStart = frameN  # exact frame index
            square.setAutoDraw(True)
        if square.status == STARTED and frameN >= (square.frameNStart + dur_square):
            square.setAutoDraw(False)

        # *text* updates
        if frameN >= dur_blank+dur_square and text.status == NOT_STARTED:
            # keep track of start time/frame for later
            text.tStart = t
            text.frameNStart = frameN  # exact frame index
            text.setAutoDraw(True)
        if text.status == STARTED and frameN >= (text.frameNStart + dur_blank):
            text.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
