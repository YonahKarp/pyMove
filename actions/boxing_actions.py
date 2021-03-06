from joint import Joint2D, noneJoint
import config

from actions.base_actions import *
from actions.hand_actions import isTrigger

from overlay import maskPointer, maskRight_jab, maskLeft_jab, putText, \
    maskUp, maskDown, maskLeft, maskRight, \
    maskLeft_AtkD, maskLeft_AtkL, maskLeft_AtkR, maskLeft_AtkU, \
    maskRight_AtkD, maskRight_AtkL, maskRight_AtkR, maskRight_AtkU
from constants import *
from Keyboard import keyboard
from controls.controlFactory import actionKeys, actionsNames

from Controller import controller


def checkForActions(frame, joints: 'list[Joint2D]', _=None):
    actions = []

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip = joints

    span = l_shoulder.dist(r_shoulder)
    r_arm = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)
    l_arm = l_shoulder.dist(l_elbow) + l_elbow.dist(l_wrist)

# Lateral Movement
    if(l_shoulder.midPointX(r_shoulder) > config.mid + .15*span):
        maskLeft(frame)
        actions.append('left')

    elif(l_shoulder.midPointX(r_shoulder) < config.mid - .15*span):
        maskRight(frame)
        actions.append('right')



# Dual Hand

    #  PAUSE
    if(shouldPause(r_wrist, l_wrist, head, span)):
        config.PAUSED = True
        config.POINTER = False
        calibrate(joints)

    # POINTER
    if(shouldPoint(r_wrist, l_wrist, head, span)):
        config.POINTER = True

    # CALIBRATE
    elif(shouldCalibrate(r_wrist, l_wrist, r_shoulder, l_shoulder, r_arm, l_arm)):
        config.calibrating = True
        putText(frame, 'calibrate', (.3, .5), CYAN)
        calibrate(joints)


# Right Hand

    elif(r_wrist.isRightOf(r_shoulder, config.r_arm*.65)):
        maskRight_AtkR(frame)
        actions.append('rhook')

    elif(
        (r_elbow.isCloseToY(r_shoulder, config.r_bicep*.35)
        and r_wrist.isAbove(r_shoulder))
        or (r_wrist.isAbove(r_shoulder))
        #    or r_wrist.isCloseTo(r_shoulder, span*.3)
    ):
        maskRight_jab(frame)
        actions.append('rjab')



# Left Hand

    elif(l_wrist.isLeftOf(l_shoulder, config.l_arm*.65)):
        maskLeft_AtkL(frame)
        actions.append('lhook')

    elif((l_elbow.isCloseToY(l_shoulder, config.l_bicep*.35) and l_wrist.isAbove(l_shoulder))
         or (l_wrist.isAbove(l_shoulder))
         #   or l_wrist.isCloseTo(l_shoulder, span*.3)

         ):
        maskLeft_jab(frame)
        actions.append('ljab')

# BLOCK
    elif(
        (r_wrist.isLeftOf(l_wrist) and r_wrist.isAbove(
            l_hip, span) and l_wrist.isAbove(l_hip, span))
        or (r_wrist.isCloseToX(l_wrist, span*.55) and r_wrist.isCloseToY(r_shoulder, span*.35) and l_wrist.isCloseToY(l_shoulder, span*.35) and r_wrist.isCloseToY(l_wrist, span*.4))
        or (r_wrist.isCloseToX(l_wrist, span*.55) and r_wrist.isAbove(r_hip, span) and l_wrist.isAbove(l_hip, span))
        or ((r_wrist.isCloseTo(r_shoulder, span*.3) or r_wrist.isCloseTo(l_shoulder, span*.3))
            and (l_wrist.isCloseTo(l_shoulder, span*.3) or l_wrist.isCloseTo(r_shoulder, span*.3)))
    ):
        putText(frame, 'block', (.4, .5), CYAN)
        actions.append('block')

    if config.DEBUG == 1:
        return []

    return actions


def pauseActions(frame, joints: 'list[Joint2D]', _=None):
    actions = []

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip = joints
    span = l_shoulder.dist(r_shoulder)
    r_arm = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)
    l_arm = l_shoulder.dist(l_elbow) + l_elbow.dist(l_wrist)

# Unpause
    if(shouldCalibrate(r_wrist, l_wrist, r_shoulder, l_shoulder, r_arm, l_arm)):
        config.PAUSED = False
        calibrate(joints)

# POINTER
    elif(shouldPoint(r_wrist, l_wrist, head, span)):
        calibrate(joints)
        config.PAUSED = False
        config.POINTER = True

    return []


def pointerActions(frame, joints: 'list[Joint2D]', hand: 'list[Joint2D]' = None):
    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip = joints


    span = l_shoulder.dist(r_shoulder)
    r_arm = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)
    l_arm = l_shoulder.dist(l_elbow) + l_elbow.dist(l_wrist)


    actions = []

    if(shouldPause(r_wrist, l_wrist, head, span)):
        config.PAUSED = True
        config.POINTER = False

    elif(shouldCalibrate(r_wrist, l_wrist, r_shoulder, l_shoulder, r_arm, l_arm)):
        config.calibrating = True
        config.POINTER = False

        putText(frame, 'calibrate', (.3, .5), CYAN)
        calibrate(joints)

    elif(l_wrist.isLeftOf(l_shoulder, config.l_arm*.7)):
        actions.append('press ab')

    coords = (r_wrist.x, r_wrist.y)


    shouldTrigger = isTrigger(hand)
    color = 0 if shouldTrigger else 1

    if(coords[0] > -1 and coords[1] > -1):
        maskPointer(frame, coords, color)
        config.mouseLocation = coords
        actions.append('move mouse')

    if(shouldTrigger):
        actions.append('press a')

    return actions


def calibrate(joints: 'list[Joint2D]'):

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, _, _, = joints

    config.height = l_shoulder.midPointY(r_shoulder)
    config.mid = l_shoulder.midPointX(r_shoulder)
    config.span = l_shoulder.dist(r_shoulder)
    config.r_bicep = r_shoulder.dist(r_elbow)
    config.l_bicep = l_shoulder.dist(l_elbow)
    config.r_forearm = r_elbow.dist(r_wrist)
    config.l_forearm = l_elbow.dist(l_wrist)
    config.r_arm = config.r_bicep + config.r_forearm
    config.l_arm = config.l_bicep + config.l_forearm
    config.calibrated = True

    for key in actionKeys:
        keyboard.KeyUp(key)
    for action in actionsNames:
        controller.actionCheck[action] = False
