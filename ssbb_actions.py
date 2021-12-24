from math import isclose
from joint import Joint2D
import config 

from overlay import putText, maskUp, maskDown, maskLeft, maskRight, maskLeft_AtkD, maskLeft_AtkL, maskLeft_AtkR, maskLeft_AtkU, maskRight_AtkD, maskRight_AtkL, maskRight_AtkR, maskRight_AtkU
from constants import *
from keyboard import keyboard
from ssbb_controls import actionKeys


actionsNames = [
    'left', 'right', 'jump', 'duck', 'block', 'hard left', 'hard right', 'start',
    'rHand jab', 'rHand right', 'rHand up', 'rHand left', 'rHand down',
    'lHand jab', 'lHand right', 'lHand up', 'lHand left', 'lHand down'
]



def checkForActions(joints : 'list[Joint2D]', frame, pressCheck):
    actions = []
    lateral_movement = ''


    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_knee, r_knee, l_ankle, r_ankle = joints

    span = l_shoulder.dist(r_shoulder)
    r_arm = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)
    l_arm = l_shoulder.dist(l_elbow) + l_elbow.dist(l_wrist)

# Lateral Movement
    if(l_shoulder.midPointX(r_shoulder) > config.mid + .75*span):
        maskLeft(frame, 1.5)
        actions.append('hard left')

    elif(l_shoulder.midPointX(r_shoulder) > config.mid + .35*span):
        maskLeft(frame)
        actions.append('left')

    elif(l_shoulder.midPointX(r_shoulder)  < config.mid - .75*span):
        maskRight(frame, 1.5)
        actions.append('hard right')
    
    elif(l_shoulder.midPointX(r_shoulder)  < config.mid - .35*span):
        maskRight(frame)
        actions.append('right')



# vertical Movement

    if(l_shoulder.y     < (config.height - .15*span)  
      and r_shoulder.y  < (config.height - .15*span)):
        maskUp(frame)
        actions.append('jump')

    if(l_shoulder.y     > (config.height + .1)  
      and r_shoulder.y  > (config.height + .1)):
        maskDown(frame)
        actions.append('duck')

# Dual Hand

    #  PAUSE
    if(r_wrist.distX(l_wrist) < span  
      and r_wrist.distY(l_wrist) < span 
      and r_wrist.isAbove(head)
      and l_wrist.isAbove(head)):
        config.PAUSED = True
        calibrate(joints, pressCheck)


    # BLOCK
    elif(r_wrist.isCloseTo(l_wrist, span*.6) and r_wrist.isAbove(r_hip) and l_wrist.isAbove(l_hip)
        or ((r_wrist.isCloseTo(r_shoulder, span*.7) or r_wrist.isCloseTo(l_shoulder, span*.7))
          and (l_wrist.isCloseTo(l_shoulder, span*.7) or l_wrist.isCloseTo(r_shoulder, span*.7)))
      ):
        putText(frame,'block',(.4,.5), CYAN)
        actions.append('block')

    # CALIBRATE
    elif(r_wrist.isRightOf(r_shoulder, r_arm*.9) 
      and l_wrist.isLeftOf(l_shoulder, l_arm*.9)):
        config.calibrating = True
        putText(frame,'calibrate',(.3,.5), CYAN)
        calibrate(joints, pressCheck)


# Right Hand

    elif(r_wrist.isAbove(r_shoulder, span*.4) 
      or (r_wrist.isAbove(r_shoulder, span*.2) and r_wrist.isRightOf(r_shoulder, span*.7))):
        maskRight_AtkU(frame)
        actions.append('rHand up')

    elif(r_wrist.isRightOf(r_shoulder, r_arm*.7)):
        maskRight_AtkR(frame)
        actions.append('rHand right')

    elif(r_wrist.isLeftOf(r_shoulder, span*.8) and r_wrist.isAbove(r_hip)):
        maskRight_AtkL(frame)
        actions.append('rHand left')

    elif( r_wrist.isBetweenX(r_shoulder, l_shoulder) 
      and r_shoulder.isBelow(l_shoulder, span*.15) and l_shoulder.y  > (config.height + span*.2)
      and r_wrist.isBelow(r_hip, span*.15) and r_wrist.isBelow(l_hip, span*.15)
    #     or 
        # (r_wrist.isRightOf(r_shoulder, r_arm*.55) and r_wrist.isBelow(r_shoulder, span*1.1)
        #   and r_wrist.isInline(r_elbow, r_shoulder, span*.2))
    #   or ((pressCheck['rHand right'] or pressCheck['rHand down'])
    #     and (r_wrist.isRightOf(r_shoulder, span*.65) and r_wrist.isBelow(r_elbow, span*.45)))
    ):
        maskRight_AtkD(frame)
        actions.append('rHand down')

    elif(r_wrist.isCloseTo(r_shoulder, span*.5)
    #   or (r_elbow.isRightOf(r_shoulder, span*.55) and r_elbow.isRightOf(r_wrist))
      ):
        maskRight_AtkD(frame)
        actions.append('rHand jab')

# Left Hand
    
    elif(l_wrist.isAbove(l_shoulder, span*.4)
      or (r_wrist.isAbove(r_shoulder, span*.2) and r_wrist.isRightOf(r_shoulder, span*.7))):
        maskLeft_AtkU(frame)
        actions.append('lHand up' + lateral_movement)

    elif(l_wrist.isLeftOf(l_shoulder, span*.9) and l_wrist.isCloseToY(l_shoulder, span*1.1)):
        maskLeft_AtkL(frame)
        actions.append('lHand left')


    elif(l_wrist.isRightOf(l_shoulder, l_arm*.7)):
        maskLeft_AtkR(frame)
        actions.append('lHand right')

    elif(l_wrist.isBetweenX(r_shoulder, l_shoulder) 
      and l_shoulder.isBelow(r_shoulder, span*.15) and r_shoulder.y  > (config.height + span*.2)
      and l_wrist.isBelow(r_hip, span*.15) and l_wrist.isBelow(l_hip, span*.15)
        # (l_wrist.isLeftOf(l_shoulder, l_arm*.55) and l_wrist.isBelow(l_shoulder, span*1.1)
        #   and l_wrist.isInline(l_elbow, l_shoulder, span*.2))
    #   and l_wrist.isCloseTo(l_hip, span*.3)
    #   or ((pressCheck['lHand left'] or pressCheck['lHand down'])
    #     and (l_wrist.isLeftOf(l_shoulder, span*.65) and l_wrist.isBelow(l_elbow, span*.45)))
    ):
        maskLeft_AtkD(frame)
        actions.append('lHand down')

    # elif((l_elbow.isLeftOf(l_shoulder, span*.55) and l_elbow.isLeftOf(l_wrist))):
    #     maskLeft_AtkD(frame)
    #     actions.append('lHand jab')

    
    if config.DEBUG == 1:
        return []

    return actions

def pauseActions(joints : 'list[Joint2D]', frame, pressCheck):
    actions = []

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_knee, r_knee, l_ankle, r_ankle = joints
    span = l_shoulder.dist(r_shoulder)
    r_arm = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)
    l_arm = l_shoulder.dist(l_elbow) + l_elbow.dist(l_wrist)

# Unpause
    if(r_wrist.isRightOf(r_shoulder, r_arm*.9) 
      and l_wrist.isLeftOf(l_shoulder, l_arm *.9)):
        config.PAUSED = False
        calibrate(joints, pressCheck)
        return []
    else:
        putText(frame,'pause',(500,200), GREEN)
    
        if(r_wrist.isRightOf(r_shoulder, span*.9)):
            maskRight_AtkR(frame)
            actions.append('start')

        return actions


def calibrate(joints : 'list[Joint2D]', pressCheck):

    _, l_shoulder, r_shoulder, _, _, _, _, _, _, _, _, _, _ = joints

    config.height = l_shoulder.midPointY(r_shoulder)
    config.mid = l_shoulder.midPointX(r_shoulder)
    for key in actionKeys:
        keyboard.KeyUp(key)
    for action in actionsNames:
        pressCheck[action] = False