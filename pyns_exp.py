"""
This code runs simple basic tasks (ie. eye open & close, blink, look left/right/up/down) to detect eye related movements/waveforms.

Use:
1. Set sequence 1, 2, 3 however you like
2. Set swtiches and change variables to vary the duration of experiment

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


##########################################
#         Experiment Parameters          #
##########################################
# 1=blinks // 2=open/close // 3=gaze
seq = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]

# switches #
netstation  = False  # False to run the file locally w/o NetStation connection
recording   = False  # True starts recording NetStation automatically

#--------------------------------------------------------------------------#
# vars             | values     | default     | description                #
#--------------------------------------------------------------------------#
dur_blank          = 0.5        # 0.5         # duration of blank transition
blink_isi          = 2                        # blink every two seconds
blink_per_block    = 4                        # N blinks per sequence
openclose_isi      = 2
openclose_per_block= 2
gaze_isi           = 1.5
gaze_per_block     = 2                        # look left, right, up, down X n

# cross size/position
cross_size         = 0.5
gaze_horizontal_pos= 13                       #cross position in cm
gaze_vertical_pos  = 10                       #cross position in cm

# miscellenious
endKey             = 'escape'                 # key to force exit
pauseKey           = 'p'                      # key to pause
mouse_visible      = False      # False       | false = mouse invisible
fixation_size      = 0.7        # 0.7         | units in cm
fullscreen         = True       # True


# shuffler
shuffle(seq)
oc_seq=[1,2]*openclose_per_block
gaze_seq=['l','r','u','d']*gaze_per_block
shuffle(gaze_seq)


##########################################
#         Initialize Components          #
##########################################
# GUI to enter subj & experiment details
gui = gui.Dlg(title="eog_blinks")
gui.addFixedField("exp:", 'eog_blinks')
gui.addField("SubjID:", '001')
gui.show()
if not gui.OK:
    print('Cancelled')
    core.quit()
exp_name = gui.data[0]
subj_id = gui.data[1]
exp_summary = exp_name + '_'  + subj_id
print('exp summary: ' + str(exp_summary))# NetStation setup


if netstation:
    import egi.simple as egi
    ms_localtime = egi.ms_localtime
    ns = egi.Netstation()
    print("Imported PyNetstation")


# create window
win = visual.Window([800,800], fullscr=fullscreen, monitor='testMonitor', color=[0,0,0], colorSpace='rgb')


stimDir = os.getcwd() # pwd/base directory
filename = os.path.join(stimDir, 'data/' + exp_summary)
if os.path.isdir(filename):
    print('DATA ALREADY EXISTS WITH SAME NAME!!! QUITTING...')
    core.quit()
if not os.path.isdir(filename):
    os.makedirs(filename)


# set text instructions
instructions = "Hello,\n\nSounds will be played, instructing what to do. \nYou will be told to OPEN/CLOSE eyes, BLINK, or LOOK at a specific direction. When looking at a specific direction, make sure you look at the direction and then LOOK BACK at the center.\n\nPress spacebar to begin."
ending = "You are done with the eye blink experiment!\n\nclosing..."


InstrText = visual.TextStim(
    win=win,text="",font='Arial',
    pos=(0, 0), height=0.9, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0,units='cm') # alignHoriz='center',alignVert='center'
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


# Sound components
sound_close = sound.Sound('./sound/close_speak.wav')
sound_close.setVolume(1)
sound_open = sound.Sound('./sound/open_speak.wav')
sound_open.setVolume(1)
sound_blink = sound.Sound('./sound/blink_speak.wav')
sound_blink.setVolume(1)
sound_left = sound.Sound('./sound/left_speak.wav')
sound_left.setVolume(1)
sound_right = sound.Sound('./sound/right_speak.wav')
sound_right.setVolume(1)
sound_up = sound.Sound('./sound/up_speak.wav')
sound_up.setVolume(1)
sound_down = sound.Sound('./sound/down_speak.wav')
sound_down.setVolume(1)


# helper functions:
def send_to_NS(type):
    if netstation:
        ns.sync()
        ns.send_event(key=str(type), timestamp=None, pad=False)
        logging.data('sent to NS: ' + str(type))


def pause_or_quit():
    if event.getKeys(keyList=[endKey]):
        print('esc quit')
        win.close()
        core.quit()
    if event.getKeys(keyList=[pauseKey]):
        event.clearEvents('keyboard')
        pauseLabel.draw()
        win.logOnFlip('paused', level=logging.DATA)
        win.flip()
        print('PAUSE')
        event.waitKeys(keyList=[pauseKey], timeStamped=globalClock)
        print('RESUME')


def blanks():
    InstrText.text = ' '
    InstrText.draw()
    win.flip()


def blank_screen():
    for frameN in range(int(round(dur_blank * 60))):
        if frameN == 0:
        #     send_to_NS(type, index)
            win.logOnFlip('start blank', level=logging.DATA)
        if frameN == int(round(dur_blank * 60)) - 1:
            win.logOnFlip('end blank', level=logging.DATA)
        pause_or_quit()
        blanks()


def show_screen():
    center.draw()
    left.draw()
    right.draw()
    up.draw()
    down.draw()
    win.logOnFlip('show screen', level=logging.DATA)
    win.flip()


# mouse cursor visibility
win.mouseVisible = mouse_visible

# set up log to keep track of all events across trials
globalClock = core.Clock()

# starts logging
logging.setDefaultClock(globalClock)
logging.console.setLevel(logging.ERROR) # logging.DATA
logDat = logging.LogFile(stimDir + '/data/' + str(exp_summary) + '/'+ str(exp_summary) + '.log', filemode='w', level=logging.DEBUG)


# Instructions
int_timer = core.Clock()
InstrText.text = instructions
InstrText.draw()
win.flip()
inst_key = event.waitKeys(keyList=['space'], timeStamped=int_timer)
pause_or_quit()


# NetStation
if netstation:
    ns.connect('10.0.0.42', 55513)
    ns.BeginSession()
    print("Connected to Netstation")
    if recording:
        ns.StartRecording()
        print("Recording ...")


##########################################
#         Begin Experiment Loop          #
##########################################
for i in range(0, len(seq)):
    blank_screen()
    # 1 = blinks
    if i == 1:
        sound_blink.setSound('./sound/blink_speak.wav')
        for i in range(0, blink_per_block):
            pause_or_quit()
            show_screen()
            core.wait(blink_isi / 2)
            sound_blink.play()
            send_to_NS('blik')
            core.wait(blink_isi / 2)

    # 2 = open/close
    if i == 2:
        sound_close.setSound('./sound/close_speak.wav')
        sound_open.setSound('./sound/open_speak.wav')
        for j in oc_seq:
            pause_or_quit()
            show_screen()
            core.wait(openclose_isi / 2)
            if j == 1:
                sound_close.play()
                send_to_NS('open')
            if j == 2:
                sound_open.play()
                send_to_NS('clos')
            core.wait(openclose_isi / 2)

    # 3 = look left/right/up/down
    if i == 3:
        sound_left.setSound('./sound/left_speak.wav')
        sound_right.setSound('./sound/right_speak.wav')
        sound_up.setSound('./sound/up_speak.wav')
        sound_down.setSound('./sound/down_speak.wav')
        for j in gaze_seq:
            pause_or_quit()
            show_screen()
            core.wait(gaze_isi / 2)
            if j == 'l':
                sound_left.play()
                send_to_NS('left')
            if j == 'r':
                sound_right.play()
                send_to_NS('rigt')
            if j == 'u':
                sound_up.play()
                send_to_NS('uupp')
            if j == 'd':
                sound_down.play()
                send_to_NS('down')
            core.wait(gaze_isi / 2)


# end the experiment
int_timer = core.Clock()
InstrText.text = ending
InstrText.draw()
win.logOnFlip('end', level=logging.DATA)
win.flip()
core.wait(2)
print('end of experiment!')

# end netstation recording
if netstation and recording:
    ns.StopRecording()

# exit out
core.wait(2)
core.quit()
