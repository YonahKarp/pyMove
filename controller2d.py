from datetime import time
import cv2
from numpy.core.defchararray import join
from src.system.interface import AnnotatorInterface
from src.utils.drawer import Drawer
import time
import numpy as np
import math

from threading import Timer


from keyboard import Keyboard
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



jointNames = ["head", "leftShoulder", "rightShoulder", "leftElbow", "rightElbow", "leftWrist", "rightWrist", "leftHip",
            "rightHip", "leftKnee", "rightKnee", "leftAnkle", "rightAnkle"]
[HEAD, LEFTSHOULDER, RIGHTSHOULDER, LEFTELBOW, RIGHTELBOW, LEFTWRIST, RIGHTWRIST, LEFTHIP,
            RIGHTHIP, LEFTKNEE, RIGHTKNEE, LEFTANKLE, RIGHTANKLE] = jointNames

height = .3
mid = .5


def start():

    annotator = AnnotatorInterface.build(max_persons=1)


    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


    # background = getBackground(cap)

    mask = np.zeros((720, 1280))
    mask[:, 0:300] = 1
    mask[:, 980:1280] = 1

    while(True):

        ret, frame = cap.read()

        if not ret:
            break

        # frame = removeBackground(frame, background)
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
            joints = dict(zip(jointNames, pose.joints))

            checkForActions(joints, frame)
        else:
            handlePresses([])


        # if DEBUG == 2:
        pressed = dict(filter(lambda e: e[1] == True, pressCheck.items()))
        cv2.putText(frame, str(pressed),(20,650), font, 1,RED,3,cv2.LINE_AA)


        if SHOW:
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            break
    
        # if cv2.waitKey(1) & 0xFF == ord('b'):
        #     background = getBackground(cap)


    annotator.terminate()
    cap.release()
    cv2.destroyAllWindows()

def getBackground(cap):

      while(True):

        ret, frame = cap.read()

        if not ret:
            break
        if cv2.waitKey(33) == ord(' '):
              return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.putText(frame,'Press Space to capture background',
            (200,200), font, 1.5,GREEN,3,cv2.LINE_AA)
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




def checkForActions(joints, frame):
    actions = []
    global height
    global mid
    global PAUSED
    shoulderSpan = abs(joints[LEFTSHOULDER][0] - joints[RIGHTSHOULDER][0])
    armSpan = bonesDist(joints[RIGHTSHOULDER], joints[RIGHTELBOW]) + bonesDist(joints[RIGHTELBOW], joints[RIGHTWRIST])
    hipSpan = abs(joints[LEFTHIP][0] - joints[RIGHTHIP][0])


    if PAUSED:
        if(joints[RIGHTWRIST][0] < joints[RIGHTSHOULDER][0] - armSpan*.7 and 
        joints[LEFTWRIST][0] > joints[LEFTSHOULDER][0] + armSpan*.5):
            cv2.putText(frame,'calibrate',(450,400), font, 2,GREEN,3,cv2.LINE_AA)
            PAUSED = False
            calibrate(joints)
        else:
            cv2.putText(frame,'pause',(500,400), font, 2,GREEN,3,cv2.LINE_AA)
            return

# Lateral Movement
    if((joints[LEFTSHOULDER][0] + joints[RIGHTSHOULDER][0])/2  > mid + .35*shoulderSpan):
        cv2.putText(frame,'left',(200,200), font, 2,GREEN,3,cv2.LINE_AA)
        actions.append('left')

    elif((joints[LEFTSHOULDER][0] + joints[RIGHTSHOULDER][0])/2  < mid - .35*shoulderSpan):
        cv2.putText(frame,'right',(200,200), font, 2,GREEN,3,cv2.LINE_AA)
        actions.append('right')


# vertical Movement

    if(joints[LEFTSHOULDER][1] < (height*.9) and 
       joints[RIGHTSHOULDER][1] < (height*.9)):
        cv2.putText(frame,'up',(200,200), font, 2,GREEN,3,cv2.LINE_AA)
        actions.append('up')

    if(joints[RIGHTSHOULDER][1]  > (height + .1) and 
       joints[LEFTSHOULDER][1] > (height + .1)):
        cv2.putText(frame,'down',(200,200), font, 2,GREEN,3,cv2.LINE_AA)
        actions.append('down')

# Dual Hand

    #  PAUSE
    if(abs(joints[RIGHTWRIST][0] - joints[LEFTWRIST][0]) < shoulderSpan and 
        abs(joints[RIGHTWRIST][1] - joints[LEFTWRIST][1]) < shoulderSpan and 
            joints[RIGHTWRIST][1] < joints[HEAD][1] and 
            joints[LEFTWRIST][1]  < joints[HEAD][1]):
             PAUSED = True
             calibrate(joints)


    # BLOCK
    elif(abs(joints[RIGHTWRIST][0] - joints[LEFTWRIST][0]) < shoulderSpan*.4 and \
        abs(joints[RIGHTWRIST][1] - joints[LEFTWRIST][1]) < shoulderSpan*.4 and \
            joints[LEFTSHOULDER][0] > joints[RIGHTWRIST][0] > joints[RIGHTSHOULDER][0] and \
            joints[RIGHTSHOULDER][0] < joints[LEFTWRIST][0] < joints[LEFTSHOULDER][0] and \
            (joints[RIGHTWRIST][1] + joints[LEFTWRIST][1])/2  < (joints[RIGHTHIP][1] + joints[LEFTHIP][1])/2):
             cv2.putText(frame,'block',(200,400), font, 2,CYAN,3,cv2.LINE_AA)
             actions.append('block')

    # CALIBRATE
    elif(joints[RIGHTWRIST][0] < joints[RIGHTSHOULDER][0] - armSpan*.7 and \
        joints[LEFTWRIST][0] > joints[LEFTSHOULDER][0] + armSpan*.5):
            cv2.putText(frame,'calibrate',(200,400), font, 2,CYAN,3,cv2.LINE_AA)
            PAUSED = False
            calibrate(joints)


# Right Hand

    elif(joints[RIGHTWRIST][1] < joints[RIGHTSHOULDER][1] - armSpan*.5):
            cv2.putText(frame,'rHand up',(200,400), font, 2,CYAN,3,cv2.LINE_AA)
            actions.append('rHand up')

    elif(joints[RIGHTWRIST][0] < joints[RIGHTSHOULDER][0] - shoulderSpan):
         cv2.putText(frame,'rHand right',(200,400), font, 2,CYAN,3,cv2.LINE_AA)
         actions.append('rHand right')


    elif(joints[RIGHTWRIST][0] > joints[RIGHTSHOULDER][0] + armSpan*.3):
         cv2.putText(frame,'rHand left',(200,400), font, 2,CYAN,3,cv2.LINE_AA)
         actions.append('rHand left')

    elif(joints[RIGHTHIP][0] < joints[RIGHTWRIST][0] < joints[LEFTHIP][0] and \
        joints[RIGHTWRIST][1] > (joints[RIGHTHIP][1] + joints[LEFTHIP][1])/2):
         cv2.putText(frame,'rHand down',(200,400), font, 2,CYAN,3,cv2.LINE_AA)
         actions.append('rHand down')

# Left Hand

    elif(joints[LEFTWRIST][1] < joints[LEFTSHOULDER][1] - armSpan*.5):
         cv2.putText(frame,'lHand up',(700,400), font, 2,CYAN,3,cv2.LINE_AA)
         actions.append('lHand up')

    elif(joints[LEFTWRIST][0] > joints[LEFTSHOULDER][0] + shoulderSpan):
         cv2.putText(frame,'lHand left',(700,400), font, 2,CYAN,3,cv2.LINE_AA)
         actions.append('lHand left')

    elif(joints[RIGHTHIP][0] < joints[LEFTWRIST][0] < joints[LEFTHIP][0] and \
        joints[LEFTWRIST][1] > (joints[RIGHTHIP][1] + joints[LEFTHIP][1])/2):
         cv2.putText(frame,'lHand down',(700,400), font, 2,CYAN,3,cv2.LINE_AA)
         actions.append('lHand down')

    elif(joints[LEFTWRIST][0] < joints[RIGHTHIP][0] ):
         cv2.putText(frame,'lHand right',(700,400), font, 2,CYAN,3,cv2.LINE_AA)
         actions.append('lHand right')

    

    
    if DEBUG == 1:
        return

    handlePresses(actions)

def bonesDist(joint1, joint2):
    return math.sqrt(((joint1[0]-joint2[0])**2)+((joint1[1]-joint2[1])**2) )


def calibrate(joints):
    global height
    global mid

    height = (joints[LEFTSHOULDER][1] + joints[RIGHTSHOULDER][1])/2
    mid = (joints[LEFTSHOULDER][0] + joints[RIGHTSHOULDER][0])/2
    for key in actionKeys:
        keyboard.KeyUp(key)
    for action in actionsNames:
        pressCheck[action] = False

actionsNames = ['left', 'right', 'up', 'down', 'block', 'rHand right', 'rHand up', 'rHand left', 'rHand down',
        'lHand right', 'lHand up', 'lHand left', 'lHand down']

actionKeys =['left', 'right', 'up', 'down', 'q', 'd', 'w', 'a', 's','z']

# pressTimer = dict(zip(actionsNames, [0]*len(actionsNames)))
# keysDict =  dict(zip(actionsNames, actionKeys))

pressCheck = dict(zip(actionsNames, [0]*len(actionsNames)))


# def handlePresses(actions):

#     for action in pressTimer:
#         if action in actions:
#             if(pressTimer[action] == 0):
#                 key = keysDict[action]
#                 splitKeys = key.split('+')
#                 if(len(splitKeys) > 1):
#                     keyboard.KeyDown(splitKeys[0])
#                     keyboard.KeyDown(splitKeys[1])
#                     keyboard.KeyUp(splitKeys[0])
#                 else:
#                     keyboard.KeyDown(key)
            
#             pressTimer[action] = 3
#         elif(pressTimer[action] > 1):
#             pressTimer[action] -= 1
#         elif(pressTimer[action] == 1):
#             pressTimer[action] -= 1
#             key = keysDict[action]
#             keyboard.KeyUp(key)

def handlePresses(actions):
    for action in actionsNames:
        config = actionCnfg[action]
        key = config['key']

        if action in actions:
            type = config['type']

            if(type == 'multi' and not pressCheck[action]):
                other = config['other']
                keyboard.KeyDown(other)
                Timer(0.3, cancelPress, (other, other)).start()

            keyboard.KeyDown(key)
            pressCheck[action] = True

            # if(type != 'sustain'):
            Timer(0.3, cancelPress, (key, action)).start()
        else:
            pressCheck[action] = False
            # keyboard.KeyUp(key)



           
            

def cancelPress(key, action):
    if(not pressCheck[action]):
        keyboard.KeyUp(key)
        print(f'cancel {key}:{action}')
    else:
        print(f'NOT CANCELED {key}:{action}')




if __name__ == "__main__":
    cv2.destroyAllWindows()

    for key in actionKeys:
        keyboard.KeyUp(key)

    print("start")
    start()



    




