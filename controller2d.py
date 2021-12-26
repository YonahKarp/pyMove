import cv2
import mediapipe as mp

import time
import numpy as np

from WebcamStream import WebcamStream

from Keyboard import keyboard
from Controller import controller
from joint import Joint2D
from overlay import putText
from ssbb_actions import calibrate, checkForActions, pauseActions

from ssbb_controls import actionKeys
from constants import *
import config 


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


font = cv2.FONT_HERSHEY_SIMPLEX

jointNames = ["head", "l_shoulder", "r_shoulder", "l_elbow", "r_elbow", "l_wrist", "r_wrist", "l_hip", "r_hip"]

def start():

    cap = WebcamStream(border=config.border, scale=config.scale).start()

    joints = [Joint2D(name, -1,-1) for name in jointNames]

    frameNum = 0
    showFrames = 2
    destroyWindow = False

    pose = mp.solutions.pose.Pose(upper_body_only=True,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.7)


    while(True):
        # print(time.time() - start)
        # start = time.time()
        frameNum += 1
            
        frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = pose.process(frame)

        frame.flags.writeable = True

        landmarks = results.pose_landmarks


    # update joints
        if(landmarks):
            tempJoints = [landmarks.landmark[i] for i in landmark_list]
            
            for i, joint in enumerate(tempJoints):
                joints[i].update(joint.x,joint.y)

            
            if(config.calibrated):
                Joint2D.calcZ(landmarks.landmark)

    # Draw joints
        if (config.SHOW > 0 and frameNum % showFrames == 0):
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if(landmarks):
                
                mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.UPPER_BODY_POSE_CONNECTIONS)

            frame = cv2.flip(frame, 1)

           
    # actions
        if(landmarks):
            frame = frame.astype(np.float32) # for overlay clipping
            actions = pauseActions(joints, frame)  if config.PAUSED \
              else checkForActions(joints, frame) 
            
            # if not config.DEBUG:
            controller.handlePresses(actions)
        else:
            controller.handlePresses([])


            
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



    




