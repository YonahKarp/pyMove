from joint import Joint2D
import config 

from overlay import maskPointer
from constants import *
from Keyboard import keyboard
from ssbb_controls import actionKeys, actionsNames

from Controller import controller

def checkForActions(joints : 'list[Joint2D]', frame):
    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip = joints

    maskPointer(frame, (r_wrist.x, r_wrist.y))

    return []
        