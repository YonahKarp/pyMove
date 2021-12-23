from math import isclose
from joint import Joint2D
import config 

from overlay import putText, maskUp, maskDown, maskLeft, maskRight, maskLeft_AtkD, maskLeft_AtkL, maskLeft_AtkR, maskLeft_AtkU, maskRight_AtkD, maskRight_AtkL, maskRight_AtkR, maskRight_AtkU
from constants import *
from keyboard import keyboard


actionsNames = [
    'left', 'right', 'up', 'down', 'block', 'hard left', 'hard right', 'm', 'start',
    'rHand jab', 'rHand right', 'rHand up', 'rHand left', 'rHand down',
    'lHand jab', 'lHand right', 'lHand up', 'lHand left', 'lHand down'
]

actionKeys =['left', 'right', 'up', 'down', 'q', 'd', 'w', 'a', 's','z', 'm']



def checkForActions(joints : 'list[Joint2D]', frame, pressCheck):
    actions = []


    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_knee, r_knee, l_ankle, r_ankle = joints

    shoulderSpan = l_shoulder.dist(r_shoulder)
    armSpan = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)

# Unpause
    if config.PAUSED:
        if(r_wrist.isRightOf(r_shoulder, armSpan*.7) 
          and l_wrist.isLeftOf(l_shoulder, armSpan*.5)):
            config.PAUSED = False
            calibrate(joints, pressCheck)
        else:
            return []

# Lateral Movement
    if(l_shoulder.midPointX(r_shoulder) > config.mid + .75*shoulderSpan):
        maskLeft(frame, 1.5)
        actions.append('hard left')

    elif(l_shoulder.midPointX(r_shoulder) > config.mid + .35*shoulderSpan):
        maskLeft(frame)
        actions.append('left')

    elif(l_shoulder.midPointX(r_shoulder)  < config.mid - .75*shoulderSpan):
        maskRight(frame, 1.5)
        actions.append('hard right')
    
    elif(l_shoulder.midPointX(r_shoulder)  < config.mid - .35*shoulderSpan):
        maskRight(frame)
        actions.append('right')


# vertical Movement

    if(l_shoulder.y     < (config.height*.9)  
      and r_shoulder.y  < (config.height*.9)):
        frame = maskUp(frame)
        actions.append('up')

    if(l_shoulder.y     > (config.height + .1)  
      and r_shoulder.y  > (config.height + .1)):
        frame = maskDown(frame)
        actions.append('down')

# Dual Hand

    #  PAUSE
    if(r_wrist.distX(l_wrist) < shoulderSpan  
      and r_wrist.distY(l_wrist) < shoulderSpan 
      and r_wrist.isAbove(head)
      and l_wrist.isAbove(head)):
        config.PAUSED = True
        calibrate(joints, pressCheck)


    # BLOCK
    elif(r_wrist.isCloseToX(l_wrist,shoulderSpan*.4)
      and r_wrist.isCloseToY(l_wrist,shoulderSpan*.4)
      and r_wrist.isLeftOf(r_shoulder)
      and l_wrist.isRightOf(l_shoulder)
      and l_wrist.midPointY(r_wrist) < l_hip.midPointY(r_hip)):
        putText(frame,'block',(.4,.5), CYAN)
        actions.append('block')

    # CALIBRATE
    elif(r_wrist.isRightOf(r_shoulder, shoulderSpan*.9) 
      and l_wrist.isLeftOf(l_shoulder, shoulderSpan*.9)):
        putText(frame,'calibrate',(.3,.5), CYAN)
        calibrate(joints, pressCheck)


# Right Hand

    elif(r_wrist.isAbove(r_shoulder, shoulderSpan*.4) 
      or (r_wrist.isAbove(r_shoulder, shoulderSpan*.2) and r_wrist.isRightOf(r_shoulder, shoulderSpan*.7))):
        maskRight_AtkU(frame)
        actions.append('rHand up')

    elif(r_wrist.isRightOf(r_shoulder, shoulderSpan*.9) and r_wrist.isCloseToY(r_shoulder, shoulderSpan*1.1)):
        maskRight_AtkR(frame)
        actions.append('rHand right')

    elif(r_wrist.isLeftOf(r_shoulder, armSpan*.3)):
        maskRight_AtkL(frame)
        actions.append('rHand left')

    elif( 
    #     (r_wrist.isBetweenX(r_shoulder, l_shoulder)  #and r_shoulder.y > (config.height + .04) 
    #   and r_shoulder.isBelow(l_shoulder, shoulderSpan*.2)
    #   and r_wrist.isBelow(r_hip, shoulderSpan*.3) or r_wrist.isBelow(l_hip, shoulderSpan*.3))
    #     or 
        (r_wrist.isRightOf(r_shoulder, shoulderSpan*.7) and r_wrist.isBelow(r_shoulder, shoulderSpan*1.1))
    #   or ((pressCheck['rHand right'] or pressCheck['rHand down'])
    #     and (r_wrist.isRightOf(r_shoulder, shoulderSpan*.65) and r_wrist.isBelow(r_elbow, shoulderSpan*.45)))
    ):
        maskRight_AtkD(frame)
        actions.append('rHand down')

    elif(r_wrist.isCloseTo(r_shoulder, shoulderSpan*.5)):
        maskRight_AtkD(frame)
        actions.append('rHand jab')

# Left Hand
    
    elif(l_wrist.isAbove(l_shoulder, shoulderSpan*.4)
      or (r_wrist.isAbove(r_shoulder, shoulderSpan*.2) and r_wrist.isRightOf(r_shoulder, shoulderSpan*.7))):
        maskLeft_AtkU(frame)
        actions.append('lHand up')

    elif(l_wrist.isLeftOf(l_shoulder, shoulderSpan*.9) and l_wrist.isCloseToY(l_shoulder, shoulderSpan*1.1)):
        maskLeft_AtkL(frame)
        actions.append('lHand left')


    elif(l_wrist.isRightOf(l_shoulder, armSpan*.3)):
        maskLeft_AtkR(frame)
        actions.append('lHand right')

    elif(
    #     l_wrist.isBetweenX(r_shoulder, l_shoulder) #and l_shoulder.y > (config.height + .04) 
    #   and l_shoulder.isBelow(r_shoulder, shoulderSpan*.2)
    #   and l_wrist.isBelow(r_hip, shoulderSpan*.3) or l_wrist.isBelow(l_hip, shoulderSpan*.3)
    #     or 
        (l_wrist.isLeftOf(l_shoulder, shoulderSpan*.7) and l_wrist.isBelow(l_shoulder, shoulderSpan*1.1))
    #   and l_wrist.isCloseTo(l_hip, shoulderSpan*.3)
    #   or ((pressCheck['lHand left'] or pressCheck['lHand down'])
    #     and (l_wrist.isLeftOf(l_shoulder, shoulderSpan*.65) and l_wrist.isBelow(l_elbow, shoulderSpan*.45)))
    ):
        maskLeft_AtkD(frame)
        actions.append('lHand down')

    # elif(l_wrist.isCloseTo(l_shoulder, shoulderSpan*.4)):
    #     maskLeft_AtkD(frame)
    #     actions.append('lHand jab')

    
    if config.DEBUG == 1:
        return []

    return actions

def pauseActions(joints : 'list[Joint2D]', frame, pressCheck):
    actions = []

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_knee, r_knee, l_ankle, r_ankle = joints
    shoulderSpan = l_shoulder.dist(r_shoulder)
    armSpan = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)

# Unpause
    if(r_wrist.isRightOf(r_shoulder, armSpan*.7) 
        and l_wrist.isLeftOf(l_shoulder, armSpan*.5)):
        config.PAUSED = False
        calibrate(joints, pressCheck)
        return []
    else:
        putText(frame,'pause',(500,200), GREEN)
    
        if(r_wrist.isRightOf(r_shoulder, shoulderSpan*.9)):
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