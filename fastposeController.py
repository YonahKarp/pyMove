from datetime import time
import cv2

from src.system.interface import AnnotatorInterface
from src.utils.drawer import Drawer
import time
import numpy as np

from WebcamStream import WebcamStream


from Keyboard import keyboard
from Controller import controller
from joint import Joint2D
from overlay import putText
from ssbb_actions import checkForActions, pauseActions

from ssbb_controls import actionCnfg, actionKeys, directionKeys
from constants import *
import config 



font = cv2.FONT_HERSHEY_SIMPLEX


jointNames = ["head", "l_shoulder", "r_shoulder", "l_elbow", "r_elbow", "l_wrist", "r_wrist", "l_hip", "r_hip", "l_knee", "r_knee", "l_ankle", "r_ankle"]

def start():

    annotator = AnnotatorInterface.build(max_persons=1, use3D = True )

    cap = WebcamStream(scale=.5).start()

    joints = [Joint2D(name, -1,-1) for name in jointNames]
    start = time.time()

    frameNum = 0
    showFrames = 2
    destroyWindow = False

    # if config.SHOW:
    #     cv2.namedWindow('frame')        # Create a named window
        # cv2.moveWindow('frame', 1700,100)  # Move it to (40,30)


    while(True):
        # print(time.time() - start)
        # start = time.time()
        frameNum += 1
            
        frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame.flags.writeable = False

        persons = annotator.update(frame)


        frame.flags.writeable = True

        poses = [p['pose_2d'] for p in persons]
        ids = [p['id'] for p in persons]

        confidence = sum(persons[0]['confidence']) if len(persons) else 0        

        if(confidence > 6.5):
            frame = Drawer.draw_scene(frame, poses, ids, _3d= persons[0]['pose_3d'])

        if config.SHOW > 0 and frameNum % showFrames == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.flip(frame, 1)


        pose = poses[0] if len(poses) else None

        # if(pose and confidence > 6.5):
        #     for i, coords in enumerate(pose.joints):
        #         joints[i].update(coords)
 
        #     frame = frame.astype(np.float32) # for overlay clipping
        #     actions = pauseActions(joints, frame)  if config.PAUSED \
        #       else checkForActions(joints, frame) 
        #     controller.handlePresses(actions)
        # else:
        #     controller.handlePresses([])

        if config.PAUSED:
            putText(frame,'pause',(.4,.5), GREEN)

        if (config.SHOW > 0 and frameNum % showFrames == 0):
            frame = np.clip(frame,0,255).astype(np.uint8) # undo from overlay clipping avoidance
            if config.DEBUG:
                frame = cv2.resize(frame, (int(frame.shape[1]*2), int(frame.shape[0]*2)), interpolation = cv2.INTER_NEAREST)
            cv2.imshow('frame', frame)
        elif not config.SHOW:
            if(config.calibrating or config.PAUSED):
                frame = np.clip(frame,0,255).astype(np.uint8) # undo from overlay clipping avoidance
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame = cv2.flip(frame, 1)
                cv2.imshow('frame', frame)
                config.calibrating = False
                destroyWindow = True
            elif(destroyWindow):
                destroyWindow = False
                cv2.destroyWindow('frame')


        if cv2.waitKey(1) & 0xFF == ord('p'):
            config.PAUSED = True


    annotator.terminate()
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    cv2.destroyAllWindows()

    for key in actionKeys:
        keyboard.KeyUp(key)


    start()



    




