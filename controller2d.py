from datetime import time
import cv2
from src.system.interface import AnnotatorInterface
from src.utils.drawer import Drawer
import time
import numpy as np
import math
from threading import Timer


from keyboard import keyboard
from joint import Joint2D
from overlay import putText
from ssbb_actions import checkForActions, pauseActions, actionsNames

from ssbb_controls import actionCnfg, actionKeys, directionKeys
from constants import *
import config 

font = cv2.FONT_HERSHEY_SIMPLEX


jointNames = ["head", "l_shoulder", "r_shoulder", "l_elbow", "r_elbow", "l_wrist", "r_wrist", "l_hip", "r_hip", "l_knee", "r_knee", "l_ankle", "r_ankle"]

def start():

    annotator = AnnotatorInterface.build(max_persons=1)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)

    # mask = np.zeros(shape)
    # mask[:, 0:250] = 1
    # mask[:, 1030:1280] = 1

    joints = [Joint2D(name, (-1,-1)) for name in jointNames]
    start = time.time()


    frameNum = 0
    showFrames = 3
    while(True):
        # print(time.time() - start)
        start = time.time()
        frameNum += 1
        
        ret, frame = cap.read()

        if not ret:
            break

        frame = frame[:, 250:frame.shape[1]-250]
        frame = cv2.resize(frame, (int(frame.shape[1]*.5), int(frame.shape[0]*.5)), interpolation = cv2.INTER_AREA)


        # frame[mask == 1] = (0,0,0)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        tmpTime = time.time()
        persons = annotator.update(frame)
        fps = int(1/(time.time()-tmpTime))

        poses = [p['pose_2d'] for p in persons]
        ids = [p['id'] for p in persons]

        confidence = sum(persons[0]['confidence']) if len(persons) else 0        

        if(confidence > 6.5):
            frame = Drawer.draw_scene(frame, poses, ids, fps, cap.get(cv2.CAP_PROP_POS_FRAMES))

        if config.SHOW and frameNum % showFrames == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.flip(frame, 1)


        pose = poses[0] if len(poses) else None

        if(pose and confidence > 6):
            for i, coords in enumerate(pose.joints):
                joints[i].update(coords)
 
            frame = frame.astype(np.float32) # for overlay clipping
            actions = pauseActions(joints, frame, actionCheck)  if config.PAUSED \
              else checkForActions(joints, frame, actionCheck) 
            handlePresses(actions)
        else:
            handlePresses([])


        # if DEBUG == 2:
        # pressed = dict(filter(lambda e: e[1] == True, pressCheck.items()))
        # putText(frame, str(pressed),(20,650),F RED, 1)


        if config.PAUSED:
            putText(frame,'pause',(.4,.5), GREEN)

        if config.SHOW and frameNum % showFrames == 0:
            frame = np.clip(frame,0,255).astype(np.uint8) # undo from overlay clipping avoidance
            if config.DEBUG:
                frame = cv2.resize(frame, (int(frame.shape[1]*2), int(frame.shape[0]*2)), interpolation = cv2.INTER_NEAREST)
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            config.PAUSED = True


    annotator.terminate()
    cap.release()
    cv2.destroyAllWindows()



actionCheck = dict(zip(actionsNames, [0]*len(actionsNames)))


def handlePresses(actions):
    keyCheck = dict(zip(actionKeys, [0]*len(actionKeys)))

    deadActions = []
    for action in actionsNames:
        config = actionCnfg[action]
        key, sustain, multi, otherKey = config.params()

        if action in actions:
            
            if(sustain):
                keyboard.KeyDown(key)
                keyCheck[key] = True

                if(multi and not keyCheck[otherKey]):
                    keyboard.KeyDown(otherKey)
                    keyCheck[otherKey] = True

            else:

            
                if(not actionCheck[action]):
                    keyboard.KeyDown(key)
                    Timer(0.25, cancelPress, (key, action)).start()
                    actionCheck[action] = True

                    if(multi and not keyCheck[otherKey]):
                        if otherKey in directionKeys:
                            for k in directionKeys:
                                keyboard.KeyUp(k)

                        keyboard.KeyDown(otherKey)
                        Timer(0.20, cancelPress, (otherKey,)).start()

                keyCheck[key] = True
                if(multi):  keyCheck[otherKey] = True


            # Timer(0.25, cancelPress, (key, action)).start()
        else:
            deadActions.append(action)

    # second loop becuase we don't want to KeyUp before we know all action input
    for action in deadActions:
        config = actionCnfg[action]

        key, sustain, multi, otherKey = config.params()

        if not keyCheck[key]:
            keyboard.KeyUp(key)

        if(multi and not keyCheck[otherKey]):
            keyboard.KeyUp(otherKey)
        

def cancelPress(key, action = None):
    keyboard.KeyUp(key)
    if action:
        actionCheck[action] = False

# def cancelPress(key, action):
#     if(not actionCheck[action]):
#         keyboard.KeyUp(key)
#     else:
#         Timer(0.25, cancelPress, (key, action)).start()

# def cancelPress(key, action):
#     if(not actionCheck[action]):
#         keyboard.KeyUp(key)
#     else:
#         Timer(0.25, cancelPress, (key, action)).start()


if __name__ == "__main__":
    cv2.destroyAllWindows()

    for key in actionKeys:
        keyboard.KeyUp(key)


    start()



    




