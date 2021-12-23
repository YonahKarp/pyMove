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
from ssbb_actions import checkForActions, pauseActions, actionsNames, actionKeys

from ssbb_controls import actionCnfg
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
    # start = time.time()


    frameNum = 0
    showFrames = 3
    while(True):
        # print(time.time() - start)
        # start = time.time()
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
            actions = pauseActions(joints, frame, pressCheck)  if config.PAUSED \
              else checkForActions(joints, frame, pressCheck) 
            handlePresses(actions)
        else:
            handlePresses([])


        # if DEBUG == 2:
        # pressed = dict(filter(lambda e: e[1] == True, pressCheck.items()))
        # putText(frame, str(pressed),(20,650), RED, 1)


        if config.PAUSED:
            putText(frame,'pause',(.4,.5), GREEN)

        if config.SHOW and frameNum % showFrames == 0:
            frame = np.clip(frame,0,255).astype(np.uint8) # undo from overlay clipping avoidance
            # frame = cv2.resize(frame, (int(frame.shape[1]*2), int(frame.shape[0]*2)), interpolation = cv2.INTER_NEAREST)
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            config.PAUSED = True


    annotator.terminate()
    cap.release()
    cv2.destroyAllWindows()



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
            Timer(0.25, cancelPress, (key, action)).start()
        else:
            pressCheck[action] = False
            # keyboard.KeyUp(key)



def cancelPress(key, action):
    if(not pressCheck[action]):
        keyboard.KeyUp(key)
    else:
        Timer(0.25, cancelPress, (key, action)).start()


if __name__ == "__main__":
    cv2.destroyAllWindows()

    for key in actionKeys:
        keyboard.KeyUp(key)


    start()



    




