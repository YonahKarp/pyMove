from datetime import time
import cv2
from src.system.interface import AnnotatorInterface
from src.utils.drawer import Drawer
import time
import numpy as np
import math
from threading import Timer


from keyboard import Keyboard
from joint import Joint2D
from overlay import *

from ssbb_controls import actionCnfg

font = cv2.FONT_HERSHEY_SIMPLEX
keyboard = Keyboard()


DEBUG = False
SHOW = True
PAUSED = True

RED = (0,0,255)
BLUE = (255,0,0)
GREEN = (0,255, 0)
CYAN = (255,255, 0)


jointNames = ["head", "l_shoulder", "r_shoulder", "l_elbow", "r_elbow", "l_wrist", "r_wrist", "l_hip", "r_hip", "l_knee", "r_knee", "l_ankle", "r_ankle"]

height = .3
mid = .5

def start():

    annotator = AnnotatorInterface.build(max_persons=1)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)

    mask = np.zeros((720, 1280))
    mask[:, 0:250] = 1
    mask[:, 1030:1280] = 1

    joints = [Joint2D(name, (-1,-1)) for name in jointNames]

    while(True):

        ret, frame = cap.read()

        if not ret:
            break

        frame[mask == 1] = (0,0,0)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        tmpTime = time.time()
        persons = annotator.update(frame)
        fps = int(1/(time.time()-tmpTime))

        poses = [p['pose_2d'] for p in persons]
        ids = [p['id'] for p in persons]
        frame = Drawer.draw_scene(frame, poses, ids, fps, cap.get(cv2.CAP_PROP_POS_FRAMES))

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)



        pose = poses[0] if len(poses) else None

        if(pose):
            for i, coords in enumerate(pose.joints):
                joints[i].update(coords)
 
            frame = frame.astype(np.float32) # for overlay clipping
            checkForActions(joints, frame)
        else:
            handlePresses([])


        # if DEBUG == 2:
        # pressed = dict(filter(lambda e: e[1] == True, pressCheck.items()))
        # putText(frame, str(pressed),(20,650), RED, 1)


        if SHOW:
            frame = np.clip(frame,0,255).astype(np.uint8) # undo from overlay clipping avoidance
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            PAUSED = True


    annotator.terminate()
    cap.release()
    cv2.destroyAllWindows()

def getBackground(cap):
      while(True):
        ret, frame = cap.read()

        if not ret:  break
        if cv2.waitKey(33) == ord(' '):
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        putText(frame,'Press Space to capture background', (200,200), GREEN)
        cv2.imshow('frame', frame)

def removeBackground(frame, background):
    θ = 40

    bwFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    binary_img = (np.abs(bwFrame.astype(np.float16) - background.astype(np.float16)) >= θ).astype(np.uint8)

    kernel = np.ones((7, 7), np.uint8)
    kernelOpen = np.ones((11,11), np.uint8)
    morph_close = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)
    morph_open = cv2.morphologyEx(morph_close, cv2.MORPH_OPEN, kernelOpen)

    frame[morph_open == 0] = RED

    return frame



def checkForActions(joints : 'list[Joint2D]', frame):
    actions = []
    global height
    global mid
    global PAUSED

    head, l_shoulder, r_shoulder, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_knee, r_knee, l_ankle, r_ankle = joints

    shoulderSpan = l_shoulder.dist(r_shoulder)
    armSpan = r_shoulder.dist(r_elbow) + r_elbow.dist(r_wrist)
    hipSpan = l_hip.dist(r_hip)

# Unpause
    if PAUSED:
        if(r_wrist.isRightOf(r_shoulder, armSpan*.7) 
          and l_wrist.isLeftOf(l_shoulder, armSpan*.5)):
            PAUSED = False
            calibrate(joints)
        else:
            putText(frame,'pause',(500,400), GREEN)
            return

# Lateral Movement
    if(l_shoulder.midPointX(r_shoulder) > mid + .7*shoulderSpan):
        maskLeft(frame, 1.5)
        actions.append('hard left')

    elif(l_shoulder.midPointX(r_shoulder) > mid + .35*shoulderSpan):
        maskLeft(frame)
        actions.append('left')

    elif(l_shoulder.midPointX(r_shoulder)  < mid - .7*shoulderSpan):
        maskRight(frame, 1.5)
        actions.append('hard right')
    
    elif(l_shoulder.midPointX(r_shoulder)  < mid - .35*shoulderSpan):
        maskRight(frame)
        actions.append('right')


# vertical Movement

    if(l_shoulder.y     < (height*.9)  
      and r_shoulder.y  < (height*.9)):
        frame = maskUp(frame)
        actions.append('up')

    if(l_shoulder.y     > (height + .1)  
      and r_shoulder.y  > (height + .1)):
        frame = maskDown(frame)
        actions.append('down')

# Dual Hand

    #  PAUSE
    if(r_wrist.distX(l_wrist) < shoulderSpan  
      and r_wrist.distY(l_wrist) < shoulderSpan 
      and r_wrist.isAbove(head)
      and l_wrist.isAbove(head)):
        PAUSED = True
        calibrate(joints)


    # BLOCK
    elif(r_wrist.isCloseToX(l_wrist,shoulderSpan*.4)
      and r_wrist.isCloseToY(l_wrist,shoulderSpan*.4)
      and r_wrist.isBetweenX(l_shoulder, r_shoulder)
      and l_wrist.isBetweenX(l_shoulder, r_shoulder)
      and l_wrist.midPointY(r_wrist) < l_hip.midPointY(r_hip)):
        putText(frame,'block',(200,400), CYAN)
        actions.append('block')

    # CALIBRATE
    elif(r_wrist.isRightOf(r_shoulder, armSpan*.7) 
      and l_wrist.isLeftOf(l_shoulder, armSpan*.5)):
        putText(frame,'calibrate',(200,400), CYAN)
        calibrate(joints)


# Right Hand

    elif(r_wrist.isAbove(r_shoulder, shoulderSpan*.5) 
      or (r_wrist.isAbove(r_shoulder, shoulderSpan*.3) and r_wrist.isRightOf(r_shoulder, shoulderSpan*.7))):
        maskRight_AtkU(frame)
        actions.append('rHand up')

    elif(r_wrist.isRightOf(r_shoulder, shoulderSpan*.9)):
        maskRight_AtkR(frame)
        actions.append('rHand right')

    elif(r_wrist.isLeftOf(r_shoulder, armSpan*.3)):
        maskRight_AtkL(frame)
        actions.append('rHand left')

    elif( (r_wrist.isBetweenX(r_hip, l_hip) and r_wrist.isBelow(r_hip) and r_wrist.isBelow(l_hip))
      or ((pressCheck['rHand right'] or pressCheck['rHand down'])
        and (r_wrist.isRightOf(r_shoulder, shoulderSpan*.65) and r_wrist.isBelow(r_elbow, shoulderSpan*.45)))
    ):
        maskRight_AtkD(frame)

        actions.append('rHand down')

# Left Hand

    elif(l_wrist.isAbove(l_shoulder, shoulderSpan*.5)
      or (r_wrist.isAbove(r_shoulder, shoulderSpan*.3) and r_wrist.isRightOf(r_shoulder, shoulderSpan*.7))):
        maskLeft_AtkU(frame)
        actions.append('lHand up')

    elif(l_wrist.isLeftOf(l_shoulder, shoulderSpan*.9)):
        maskLeft_AtkL(frame)
        actions.append('lHand left')


    elif(l_wrist.isRightOf(l_shoulder, armSpan*.3)):
        maskLeft_AtkR(frame)
        actions.append('lHand right')

    elif(l_wrist.isBetweenX(r_hip, l_hip) and l_shoulder.y > (height + .04) and l_wrist.isBelow(r_hip) and l_wrist.isBelow(l_hip)
      or ((pressCheck['lHand left'] or pressCheck['lHand down'])
        and (l_wrist.isLeftOf(l_shoulder, shoulderSpan*.65) and l_wrist.isBelow(l_elbow, shoulderSpan*.45)))
    ):
        maskLeft_AtkD(frame)
        actions.append('lHand down')

    
    if DEBUG == 1:
        return

    handlePresses(actions)

def bonesDist(joint1, joint2):
    return math.sqrt(((joint1[0]-joint2[0])**2)+((joint1[1]-joint2[1])**2) )


def calibrate(joints : 'list[Joint2D]'):
    global height
    global mid

    _, l_shoulder, r_shoulder, _, _, _, _, _, _, _, _, _, _ = joints

    height = l_shoulder.midPointY(r_shoulder)
    mid = l_shoulder.midPointX(r_shoulder)
    for key in actionKeys:
        keyboard.KeyUp(key)
    for action in actionsNames:
        pressCheck[action] = False

actionsNames = ['left', 'right', 'up', 'down', 'block', 'rHand right', 'rHand up', 'rHand left', 'rHand down',
        'lHand right', 'lHand up', 'lHand left', 'lHand down', 'hard left', 'hard right', 'm']

actionKeys =['left', 'right', 'up', 'down', 'q', 'd', 'w', 'a', 's','z', 'm']


pressCheck = dict(zip(actionsNames, [0]*len(actionsNames)))

def handlePresses(actions):
    for action in actionsNames:
        config = actionCnfg[action]
        key = config['key']

        if action in actions:
            type = config['type']

            if(type == 'multi' and not pressCheck[action]):
                otherKey = config['otherKey']
                otherAction = config['otherAction']
                keyboard.KeyDown(otherKey)
                Timer(0.25, cancelPress, (otherKey, otherAction)).start()

            keyboard.KeyDown(key)
            pressCheck[action] = True

            # if(type != 'sustain'):
            Timer(0.25, cancelPress, (key, action)).start()
        else:
            pressCheck[action] = False
            # keyboard.KeyUp(key)



def cancelPress(key, action):
    if(not pressCheck[action]):
        keyboard.KeyUp(key)
        # print(f'cancel {key}:{action}')
    else:
        Timer(0.25, cancelPress, (key, action)).start()
        # print(f'NOT CANCELED {key}:{action}')


if __name__ == "__main__":
    cv2.destroyAllWindows()

    for key in actionKeys:
        keyboard.KeyUp(key)


    start()



    




