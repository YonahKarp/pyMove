from profiler import profile
import cv2
import mediapipe as mp
import sys

import time
import numpy as np

from WebcamStream import WebcamStream

from Keyboard import keyboard
from Controller import controller
from joint import Joint2D
from overlay import putText
from constants import *
import config 
from actions.actionFactory import pointerActions, checkForActions, pauseActions
from controls.controlFactory import actionKeys

import landmark_utils
from landmark_utils import jointNames, hand_names


mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

solution = mp.solutions.pose.Pose if config.GAME in ['SSBB'] \
            else mp.solutions.holistic.Holistic

def start():

    cap = WebcamStream(border=config.border).start()

    joints =    [Joint2D(name, -1,-1) for name in jointNames]
    hand =      [Joint2D(name, -1,-1) for name in hand_names]

    frameNum = 0
    showFrames = 2
    destroyWindow = False

    pose = solution(upper_body_only=True,
        min_detection_confidence=0.3,
        min_tracking_confidence=0.5)

    # start = time.time()

    while(True):
        # print(time.time() - start)
        # start = time.time()

        frameNum += 1
            
        print(cap.hasNew)
        frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        # start = time.time()
        results = pose.process(frame)
        # print(time.time() - start)
        frame.flags.writeable = True

        landmarks = results.pose_landmarks
        r_hand_landmarks = results.right_hand_landmarks \
            if hasattr(results, 'right_hand_landmarks') \
                else None

    # update joints
        if(landmarks):
            tempJoints = [landmarks.landmark[i] for i in landmark_list]
            
            for i, joint in enumerate(tempJoints):
                joints[i].update(joint.x,joint.y)

            # if(config.calibrated):
            #     Joint2D.calcZ(landmarks.landmark, joints)

        if(r_hand_landmarks):
            tempHand = [r_hand_landmarks.landmark[i] for i in hand_list]
            for i, finger in enumerate(tempHand):
                hand[i].update(finger.x,finger.y, finger.z)
        


    # Draw joints
        if (config.SHOW > 0 and frameNum % showFrames == 0):
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if(landmarks):
                landmark_utils.hideUnwanted(landmarks.landmark, landmark_list)
                mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.UPPER_BODY_POSE_CONNECTIONS)

            if(r_hand_landmarks):
                # landmark_utils.hideUnwanted(r_hand_landmarks.landmark, hand_list)
                mp_drawing.draw_landmarks(frame,r_hand_landmarks,mp_holistic.HAND_CONNECTIONS)

            frame = cv2.flip(frame, 1)

           
    # actions
        # start = time.time()
        if(landmarks):
            frame = frame.astype(np.float32) # for overlay clipping
            actions = pauseActions(frame, joints)  if config.PAUSED \
                else pointerActions(frame, joints, hand) if config.POINTER \
                else checkForActions(frame, joints, hand) 
                
            
            # if not config.DEBUG: 
            controller.handlePresses(actions)
        else:
            controller.handlePresses([])
        # print(time.time() - start)



            
    # Display window
        if config.PAUSED:
            putText(frame,'pause',(.4,.5), GREEN)

        if (config.SHOW > 0 and frameNum % showFrames == 0):
            frame = np.clip(frame,0,255).astype(np.uint8) # undo from overlay clipping avoidance
            if config.DEBUG:
                frame = cv2.resize(frame, (int(frame.shape[1]*(1/config.scale)), int(frame.shape[0]*(1/config.scale))), interpolation = cv2.INTER_NEAREST)
            cv2.imshow('frame', frame)
        elif not config.SHOW:
            if(config.calibrating or config.PAUSED):

                frame = np.clip(frame,0,255).astype(np.uint8) # undo from overlay clipping avoidance
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame = cv2.resize(frame, (int(frame.shape[1]*(1/config.scale)), int(frame.shape[0]*(1/config.scale))), interpolation = cv2.INTER_NEAREST)

                if(landmarks):  
                    mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.UPPER_BODY_POSE_CONNECTIONS)
                frame = cv2.flip(frame, 1)
                
                cv2.imshow('frame', frame)
                cv2.waitKey(1) 
                config.calibrating = False
                destroyWindow = True
            elif(destroyWindow):
                destroyWindow = False
                cv2.destroyWindow('frame')
                cv2.waitKey(1)
            


        if config.SHOW and (cv2.waitKey(1) & 0xFF == ord('p')):
            break


    cv2.destroyAllWindows()
    cap.stopped = True
    print('done')



if __name__ == "__main__":
    if(len(sys.argv) > 1):
        config.SHOW = config.DEBUG = int(sys.argv[1])

    cv2.destroyAllWindows()

    for key in actionKeys:
        keyboard.KeyUp(key, True)

    start()

