from joint import Joint2D, noneJoint
import config

from actions.base_actions import *
import actions.hand_actions as handActions

from overlay import maskPointer, maskRight_jab, maskLeft_jab, putText, \
    maskUp, maskDown, maskLeft, maskRight, \
    maskLeft_AtkD, maskLeft_AtkL, maskLeft_AtkR, maskLeft_AtkU, \
    maskRight_AtkD, maskRight_AtkL, maskRight_AtkR, maskRight_AtkU
from constants import *
from Keyboard import keyboard
from controls.controlFactory import actionKeys, actionsNames

from Controller import controller


def checkForActions(frame, joints: 'list[Joint2D]', hand=None):
    actions = []

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip = joints

    span = l_shoulder.dist(r_shoulder)
    h_span = l_hip.dist(r_hip)
    torso = r_hip.distY(r_shoulder)

    r_arm = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)
    l_arm = l_shoulder.dist(l_elbow) + l_elbow.dist(l_wrist)

# Lateral Movement
    if(l_shoulder.midPointX(r_shoulder) > config.mid + .35*span):
        maskLeft(frame)
        actions.append('left')

    elif(l_shoulder.midPointX(r_shoulder) < config.mid - .35*span):
        maskRight(frame)
        actions.append('right')

# z- movement
    if(h_span < config.h_span*.85 and torso < config.torso*.85):
        maskDown(frame)
        actions.append('back')

    elif(span > config.span*1.1 and torso > config.torso*1.1):
        maskDown(frame, 2)
        actions.append('fwd')



# vertical Movement

    if(l_shoulder.y < (config.height - .2*span) and r_shoulder.y < (config.height - .2*span)
        and l_hip.y < (config.h_height - .2*span) and r_hip.y < (config.h_height - .2*span)):
        maskUp(frame)
        actions.append('jump')

    if(l_shoulder.y     > (config.height + .1)  
      and r_shoulder.y  > (config.height + .1)):
        maskDown(frame)
        actions.append('morph')


# Dual Hand


    coords = (r_wrist.x, r_wrist.y)
    isTrigger = handActions.isTrigger(hand)
    color = 0 if isTrigger else 1


    #  PAUSE
    if(shouldPause(r_wrist, l_wrist, head, span)):
        config.PAUSED = True
        calibrate(joints)

    # CALIBRATE
    elif(shouldCalibrate(r_wrist, l_wrist, r_shoulder, l_shoulder, r_arm, l_arm)):
        config.calibrating = True
        putText(frame, 'calibrate', (.3, .5), CYAN)
        calibrate(joints)

    
    if(coords[0] > -1 and coords[1] > -1):
        maskPointer(frame, coords, color)
        config.mouseLocation = coords
        actions.append('move mouse')

    if(isTrigger):
        actions.append('fire')

    

    

# Right Hand



# Left Hand
    

    if(l_wrist.isCloseTo(r_wrist, span*.5) or l_wrist.isCloseTo(r_elbow, span*.5)):
        maskLeft_AtkR(frame)
        actions.append('lock')

    elif(l_wrist.isCloseToY(head, span*.25) 
        and not l_wrist.isCloseToX(head, span*.25)
        and l_wrist.isLeftOf(head, span*.35)
        and not l_wrist.isLeftOf(head, span*.7)
        
        and not r_wrist.isCloseTo(l_wrist, span*.3)):
        maskLeft_jab(frame)
        actions.append('visor')

    # elif(l_wrist.isLeftOf(l_shoulder, config.l_arm*.7)):
    #     maskLeft_AtkL(frame)
    #     actions.append('map')

    elif(l_wrist.isBetweenX(r_shoulder, l_shoulder) 
      and l_shoulder.isBelow(r_shoulder, span*.15) and r_shoulder.y  > (config.height + span*.2)
      and l_wrist.isBelow(r_hip, span*.15) and l_wrist.isBelow(l_hip, span*.15)
    ):
        maskLeft_AtkD(frame)
        actions.append('missle')



# BLOCK
    # elif(
    #     (r_wrist.isLeftOf(l_wrist) and r_wrist.isAbove(
    #         l_hip, span) and l_wrist.isAbove(l_hip, span))
    #     or (r_wrist.isCloseToX(l_wrist, span*.55) and r_wrist.isCloseToY(r_shoulder, span*.35) and l_wrist.isCloseToY(l_shoulder, span*.35) and r_wrist.isCloseToY(l_wrist, span*.4))
    #     or (r_wrist.isCloseToX(l_wrist, span*.55) and r_wrist.isAbove(r_hip, span) and l_wrist.isAbove(l_hip, span))
    #     or ((r_wrist.isCloseTo(r_shoulder, span*.3) or r_wrist.isCloseTo(l_shoulder, span*.3))
    #         and (l_wrist.isCloseTo(l_shoulder, span*.3) or l_wrist.isCloseTo(r_shoulder, span*.3)))
    # ):
    #     putText(frame, 'morph', (.4, .5), CYAN)
    #     actions.append('morph')


        # TO:DO change modes in config?

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

    return []

def pointerActions(frame, joints: 'list[Joint2D]', _=None, hand = None):
     return []


def calibrate(joints: 'list[Joint2D]'):

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, = joints

    config.height = l_shoulder.midPointY(r_shoulder)
    config.mid = l_shoulder.midPointX(r_shoulder)
    config.span = l_shoulder.dist(r_shoulder)
    config.h_span = l_hip.dist(r_hip)
    config.h_height = l_hip.midPointY(r_hip)
    config.torso = r_hip.distY(r_shoulder)

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
