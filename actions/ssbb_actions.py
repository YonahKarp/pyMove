from joint import Joint2D, noneJoint
from DolphinControls import Stick
import config 

from overlay import maskPointer, maskRight_jab, maskLeft_jab, putText, \
    maskUp, maskDown, maskLeft, maskRight, \
    maskLeft_AtkD, maskLeft_AtkL, maskLeft_AtkR, maskLeft_AtkU, \
    maskRight_AtkD, maskRight_AtkL, maskRight_AtkR, maskRight_AtkU
from constants import *
# from Keyboard import keyboard
from DolphinControls import dolphinControls
from controls.controlFactory import actionKeys, actionsNames

from Controller import controller

def checkForActions(frame, joints : 'list[Joint2D]', _=None):
    actions = []
    lateral_movement = ''
    movement_hard = False

    config.sticks[Stick.MAIN] = [.5,.5]
    config.sticks[Stick.C] = [.5,.5]


    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip = joints

    span = l_shoulder.dist(r_shoulder)
    r_arm = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)
    l_arm = l_shoulder.dist(l_elbow) + l_elbow.dist(l_wrist)

# Lateral Movement
    # if(l_shoulder.midPointX(r_shoulder) > config.mid + .75*span):
    #     maskLeft(frame, 1.5)
    #     actions.append('hard left')
    #     lateral_movement = '_left'
    #     movement_hard = True

    movement = l_shoulder.midPointX(r_shoulder) - config.mid
    if(movement > .3*span):
        config.sticks[Stick.MAIN][0] = .5 - min((abs(movement) - .3*span)/(2*(.7*span - .3*span)),.5)
        maskLeft(frame)
        actions.append('left')
        lateral_movement = '_left'

    # elif(l_shoulder.midPointX(r_shoulder)  < config.mid - .75*span):
    #     maskRight(frame, 1.5)
    #     actions.append('hard right')
    #     lateral_movement = '_right'
    #     movement_hard = True
    
    elif(movement < - .3*span):
        config.sticks[Stick.MAIN][0] = .5 + min((abs(movement) - .3*span)/ (2*(.7*span - .3*span)),.5)
        maskRight(frame)
        actions.append('right')
        lateral_movement = '_right'


# vertical Movement

    if(l_shoulder.y     < (config.height - .1*span)  
      and r_shoulder.y  < (config.height - .1*span)):
        maskUp(frame)
        actions.append('jump')

    if(l_shoulder.y     > (config.height + .15)  
      and r_shoulder.y  > (config.height + .15)):
        maskDown(frame)
        config.sticks[Stick.MAIN][1] = 1
        actions.append('duck')

# Dual Hand

    #  PAUSE
    if(r_wrist.distX(l_wrist) < span  
      and r_wrist.distY(l_wrist) < span 
      and r_wrist.isAbove(head)
      and l_wrist.isAbove(head)):
        config.PAUSED = True
        calibrate(joints)


    # BLOCK
    elif((r_wrist.isCloseToX(l_wrist, span*.6) and r_wrist.isCloseToY(l_wrist, span*.3) and r_wrist.isCloseToY(r_shoulder, span*.4) and l_wrist.isCloseToY(l_shoulder, span*.4)  )
        or (r_wrist.isCloseToX(l_wrist, span*.6) and r_wrist.isCloseToY(l_wrist, span*.3) and r_wrist.isAbove(r_hip, span*.9) and l_wrist.isAbove(l_hip, span*.9))
        or (r_wrist.isCloseTo(r_shoulder, span*.3) and l_wrist.isCloseTo(r_shoulder, span*.3))
        or (l_wrist.isCloseTo(l_shoulder, span*.3) and r_wrist.isCloseTo(l_shoulder, span*.3))
        # or (r_wrist.isLeftOf(l_wrist) and r_wrist.isAbove(r_hip, span*.9) and l_wrist.isAbove(l_hip, span*.9) )
      ):
        putText(frame,'block',(.4,.5), CYAN)
        actions.append('block')

    # CALIBRATE
    elif(r_wrist.isRightOf(r_shoulder, r_arm*.9) 
      and l_wrist.isLeftOf(l_shoulder, l_arm*.9)):
        config.calibrating = True
        putText(frame,'calibrate',(.3,.5), CYAN)
        calibrate(joints)


# Right Hand

    elif(r_wrist.isAbove(r_shoulder, span*.1) and r_elbow.isAbove(r_shoulder, span*.1) 
      and r_wrist.isCloseToY(r_elbow, config.span*.4)
      and r_wrist.isLeftOf(r_elbow, config.r_forearm*.7)
      and r_wrist.isLeftOf(head, -config.span*.2)
    #   or (r_wrist.isAbove(r_shoulder, span*.2) and r_wrist.isRightOf(r_shoulder, span*.7))
      ):
        # maskRight_AtkU(frame)
        maskRight_jab(frame)
        config.sticks[Stick.MAIN][1] = 0
        actions.append('rHand uptilt')
        actions.append('up')


    elif(r_wrist.isAbove(head, span*.25) 
    #   or (r_wrist.isAbove(r_shoulder, span*.2) and r_wrist.isRightOf(r_shoulder, span*.7))
      ):
        maskRight_AtkU(frame)
        config.sticks[Stick.C][1] = 0
        actions.append('rHand up')

    elif(r_wrist.isRightOf(r_shoulder, config.r_arm*.7)):
        maskRight_AtkR(frame)
        config.sticks[Stick.C][0] = 1
        actions.append('rHand right')

    elif(r_wrist.isLeftOf(r_shoulder, span*.9) and r_wrist.isAbove(r_hip)):
        maskRight_AtkL(frame)
        config.sticks[Stick.C][0] = 0
        actions.append('rHand left')

    elif( r_wrist.isBetweenX(r_shoulder, l_shoulder) 
      and r_shoulder.isBelow(l_shoulder, span*.1) and l_shoulder.y  > (config.height + span*.1)
      and r_wrist.isBelow(r_hip, span*.15) and r_wrist.isBelow(l_hip, span*.15)
    #     or 
        # (r_wrist.isRightOf(r_shoulder, r_arm*.55) and r_wrist.isBelow(r_shoulder, span*1.1)
        #   and r_wrist.isInline(r_elbow, r_shoulder, span*.2))
    ):
        maskRight_AtkD(frame)
        config.sticks[Stick.C][1] = 1
        actions.append('rHand down')

    # elif(
    #     r_wrist.isInFrontOf(r_elbow, config.r_forearm*.9) and r_wrist.isBelow(r_shoulder, span*1.2 )
    # #   or
    # #    (r_elbow.isRightOf(r_shoulder, span*.55) and r_elbow.isRightOf(r_wrist, r_wrist.dist(r_elbow)*.6))
    #   ):
    #     maskRight_jab(frame)
    #     actions.append('rHand jab')

# Left Hand

    elif(l_wrist.isAbove(l_shoulder, span*.1) and l_elbow.isAbove(l_shoulder, span*.1) 
      and l_wrist.isCloseToY(l_elbow, config.span*.35)
      and l_wrist.isRightOf(l_elbow, config.l_forearm*.7)
      and l_wrist.isRightOf(head, -config.span*.2) and l_wrist.isBelow(head, -config.span*.1)
    #   or (r_wrist.isAbove(r_shoulder, span*.2) and r_wrist.isRightOf(r_shoulder, span*.7))
      ):
        # maskRight_AtkU(frame)
        maskLeft_jab(frame)
        actions.append('lHand jab')
    
    elif(l_wrist.isAbove(head, span*.25)
    #   or (r_wrist.isAbove(r_shoulder, span*.2) and r_wrist.isRightOf(r_shoulder, span*.7))
      ):
        maskLeft_AtkU(frame)
        config.sticks[Stick.MAIN][1] = 0
        if(lateral_movement == '_left'): config.sticks[Stick.MAIN][0] = 0
        if(lateral_movement == '_right'): config.sticks[Stick.MAIN][0] = 1


        actions.append('lHand up')


    elif(l_wrist.isLeftOf(l_shoulder, config.l_arm*.7) 
      # and not movement_hard
    ):
        maskLeft_AtkL(frame)
        config.sticks[Stick.MAIN][0] = .3
        actions.append('lHand left')


    elif(l_wrist.isRightOf(l_shoulder, span*.9) and l_wrist.isAbove(l_hip)):
        maskLeft_AtkR(frame)
        config.sticks[Stick.MAIN][0] = .7
        actions.append('lHand right')

    elif(l_wrist.isBetweenX(r_shoulder, l_shoulder) 
      and l_shoulder.isBelow(r_shoulder, span*.15) and r_shoulder.y  > (config.height + span*.2)
      and l_wrist.isBelow(r_hip, span*.15) and l_wrist.isBelow(l_hip, span*.15)
        # (l_wrist.isLeftOf(l_shoulder, l_arm*.55) and l_wrist.isBelow(l_shoulder, span*1.1)
        #   and l_wrist.isInline(l_elbow, l_shoulder, span*.2))
    #   and l_wrist.isCloseTo(l_hip, span*.3)
    ):
        maskLeft_AtkD(frame)
        config.sticks[Stick.MAIN][1] = 1
        actions.append('lHand down')

    # elif(
    #      l_wrist.isCloseTo(l_shoulder, span*.7) and l_wrist.isInFrontOf(l_hip, .7)
    #     ):
    #     maskLeft_jab(frame)
    #     actions.append('lHand jab')

    
    # if config.DEBUG == 1:
    #     return []

    return actions

def pauseActions(frame, joints : 'list[Joint2D]', _=None):
    actions = []

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip = joints
    span = l_shoulder.dist(r_shoulder)
    r_arm = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)
    l_arm = l_shoulder.dist(l_elbow) + l_elbow.dist(l_wrist)

# Unpause
    if(r_wrist.isRightOf(r_shoulder, r_arm*.9) 
      and l_wrist.isLeftOf(l_shoulder, l_arm *.9)):
        config.PAUSED = False
        calibrate(joints)
    
    return []
    # else:
    #     putText(frame,'pause',(500,200), GREEN)
    
    #     if(r_wrist.isRightOf(r_shoulder, span*.9)):
    #         maskRight_AtkR(frame)
    #         actions.append('start')

    #     return actions

def pointerActions(frame, joints : 'list[Joint2D]', hand : 'list[Joint2D]' = None):
    return []



def calibrate(joints : 'list[Joint2D]'):

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, _, _, = joints

    config.height = l_shoulder.midPointY(r_shoulder)
    config.mid = l_shoulder.midPointX(r_shoulder)
    config.span = l_shoulder.dist(r_shoulder)
    config.r_bicep = r_shoulder.dist(r_elbow)
    config.l_bicep = l_shoulder.dist(l_elbow)
    config.r_forearm =  r_elbow.dist(r_wrist)
    config.l_forearm =  l_elbow.dist(l_wrist)
    config.r_arm = config.r_bicep + config.r_forearm
    config.l_arm = config.l_bicep + config.l_forearm
    config.calibrated = True

    # for key in actionKeys:
    #     keyboard.KeyUp(key)
    dolphinControls.reset()
    
    for action in actionsNames:
        controller.actionCheck[action] = False