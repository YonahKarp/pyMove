import cv2
import numpy as np


font = cv2.FONT_HERSHEY_SIMPLEX

black_width = 250

lMask = np.array([np.arange(100, 0, -0.5) for _ in range(0, 720)])
rMask = np.array([np.arange(0, 100, 0.5) for _ in range(0, 720)])
uMask = np.array([np.arange(100, 0, -1) for _ in range(0, 1280)]).T
dMask = np.array([np.arange(0, 100, 1) for _ in range(0, 1280)]).T

a_rMask = np.array([np.arange(0, 100, 1) for _ in range(0, 300)])
a_lMask = np.array([np.arange(100, 0, -1) for _ in range(0, 300)])
a_dMask = np.array([np.arange(0, 100, 1) for _ in range(0, 500)]).T
a_uMask = np.array([np.arange(100, 0, -1) for _ in range(0, 500)]).T


def putText(frame, text, coords, color, scale = 2):
    cv2.putText(frame, text, coords, font, scale, color, 3, cv2.LINE_AA)

def maskLeft(frame, multiplyer=1):
    frame[:, 0:200, 1] = frame[:, 0:200, 1] + (lMask * multiplyer)
    return np.clip(frame, 0, 255)
def maskRight(frame, multiplyer=1):
    frame[:, 1080:1280, 1] = frame[:, 1080:1280, 1] + (rMask * multiplyer)
    return np.clip(frame, 0, 255)
def maskUp(frame):
    frame[0:100, :, 1] = frame[0:100, :, 1] + uMask 
    return np.clip(frame, 0, 255)
def maskDown(frame):
    frame[620:720, :, 1] = frame[620:720, :, 1] + dMask 
    return np.clip(frame, 0, 255)

# Attack Masks
def maskRight_AtkR(frame):
    frame[210:510, 930:1030, 2] = frame[210:510,  930:1030, 2] + a_rMask
    return np.clip(frame, 0, 255)
def maskRight_AtkL(frame):
    frame[210:510, 250:350, 2] = frame[210:510,  250:350, 2] + a_lMask
    return np.clip(frame, 0, 255)
def maskRight_AtkU(frame):
    frame[0:100, 390:890, 2] = frame[0:100, 390:890, 2] + a_uMask
    return np.clip(frame, 0, 255)
def maskRight_AtkD(frame):
    frame[620:720, 390:890, 2] = frame[620:720, 390:890, 2] + a_dMask
    return np.clip(frame, 0, 255)

# Special Masks
def maskLeft_AtkR(frame):
    frame[210:510, 930:1030, 0] = frame[210:510,  930:1030, 0] + a_rMask
    return np.clip(frame, 0, 255)
def maskLeft_AtkL(frame):
    frame[210:510, 250:350, 0] = frame[210:510,  250:350, 0] + a_lMask
    return np.clip(frame, 0, 255)
def maskLeft_AtkU(frame):
    frame[0:100, 390:890, 0] = frame[0:100, 390:890, 0] + a_uMask
    return np.clip(frame, 0, 255)
def maskLeft_AtkD(frame):
    frame[620:720, 390:890, 0] = frame[620:720, 390:890, 0] + a_dMask
    return np.clip(frame, 0, 255)
