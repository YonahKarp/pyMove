import cv2
import numpy as np
import config


# Utils
def circularMask(h,w, cy, cx, r):
    x = np.arange(0, w)
    y = np.arange(0, h)

    return (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < r**2

font = cv2.FONT_HERSHEY_SIMPLEX

gap = 0

scale = config.scale
h = int(720*scale)
w = int(880*scale)

# h = 360
# w = 390

W = int(w*.6)
H = int(h*.6)

atkW = int((w-W)/2)
atkH = int((h-H)/2)

maskW = int(200*scale)

lMask = np.array([np.arange(maskW, 0, -0.5) for _ in range(0, h)])
rMask = np.array([np.arange(0, maskW, 0.5) for _ in range(0, h)])
uMask = np.array([np.arange(maskW, 0, -1) for _ in range(0, w)]).T
dMask = np.array([np.arange(0, maskW, 1) for _ in range(0, w)]).T

a_rMask = np.array([np.arange(0, maskW, 1) for _ in range(0, h-2*atkH)])
a_lMask = np.array([np.arange(maskW, 0, -1) for _ in range(0, h-2*atkH)])
a_dMask = np.array([np.arange(0, maskW, 1) for _ in range(0, w-2*atkW)]).T
a_uMask = np.array([np.arange(maskW, 0, -1) for _ in range(0, w-2*atkW)]).T



a_jabMask = circularMask(h,w, int(h/3), int(w/1.5), int(maskW/2))
b_jabMask = circularMask(h,w, int(h/3), int(w/3), int(maskW/2))



def putText(frame, text, coords, color, scale = 1):
    coords = (int(coords[0]*w), int(coords[1]*h))
    cv2.putText(frame, text, coords, font, scale, color, 2, cv2.LINE_AA)

def maskLeft(frame, multiplyer=1):
    frame[:, 0:maskW*2, 1] = frame[:, 0:maskW*2, 1] + (lMask * multiplyer)
    return np.clip(frame, 0, 255)
def maskRight(frame, multiplyer=1):
    frame[:, w-maskW*2:w, 1] = frame[:, w-maskW*2:w, 1] + (rMask * multiplyer)
    return np.clip(frame, 0, 255)
def maskUp(frame):
    frame[0:maskW, :, 1] = frame[0:maskW, :, 1] + uMask 
    return np.clip(frame, 0, 255)
def maskDown(frame):
    frame[h-maskW:h, :, 1] = frame[h-maskW:h, :, 1] + dMask 
    return np.clip(frame, 0, 255)

# Attack Masks
def maskRight_AtkR(frame):
    frame[atkH:h-atkH,  w-(gap+maskW):w-gap, 2] = frame[atkH:h-atkH,  w-(gap+maskW):w-gap, 2] + a_rMask
    return np.clip(frame, 0, 255)
def maskRight_AtkL(frame):
    frame[atkH:h-atkH, gap:gap+maskW, 2] = frame[atkH:h-atkH,  gap:gap+maskW, 2] + a_lMask
    return np.clip(frame, 0, 255)
def maskRight_AtkU(frame):
    frame[0:maskW, atkW:w-atkW, 2] = frame[0:maskW, atkW:w-atkW, 2] + a_uMask
    return np.clip(frame, 0, 255)
def maskRight_AtkD(frame):
    frame[h-maskW:h, atkW:w-atkW, 2] = frame[h-maskW:h, atkW:w-atkW, 2] + a_dMask
    return np.clip(frame, 0, 255)



def maskRight_jab(frame):
    frame[a_jabMask, 2] = frame[a_jabMask, 2] + 150
    return np.clip(frame, 0, 255)

    
# Special Masks
def maskLeft_AtkR(frame):
    frame[atkH:h-atkH,  w-(gap+maskW):w-gap, 0] = frame[atkH:h-atkH,  w-(gap+maskW):w-gap, 0] + a_rMask
    return np.clip(frame, 0, 255)
def maskLeft_AtkL(frame):
    frame[atkH:h-atkH, gap:gap+maskW, 0] = frame[atkH:h-atkH,  gap:gap+maskW, 0] + a_lMask
    return np.clip(frame, 0, 255)
def maskLeft_AtkU(frame):
    frame[0:maskW, atkW:w-atkW, 0] = frame[0:maskW, atkW:w-atkW, 0] + a_uMask
    return np.clip(frame, 0, 255)
def maskLeft_AtkD(frame):
    frame[h-maskW:h, atkW:w-atkW, 0] = frame[h-maskW:h, atkW:w-atkW, 0] + a_dMask
    return np.clip(frame, 0, 255)


def maskLeft_jab(frame):
    frame[b_jabMask, 0] = frame[b_jabMask, 0] + 150
    return np.clip(frame, 0, 255)


# Don't show masks
if config.SHOW < 2 :
    def putText(frame, text, coords, color, scale = 2): pass
    def maskLeft(frame, multiplyer=1): pass
    def maskRight(frame, multiplyer=1): pass
    def maskUp(frame): pass
    def maskDown(frame): pass
    def maskRight_AtkR(frame): pass
    def maskRight_AtkL(frame): pass
    def maskRight_AtkU(frame): pass
    def maskRight_AtkD(frame): pass
    def maskLeft_AtkR(frame): pass
    def maskLeft_AtkL(frame): pass
    def maskLeft_AtkU(frame): pass
    def maskLeft_AtkD(frame): pass
    def maskRight_jab(frame): pass
    def maskLeft_jab(frame): pass





if __name__ == "__main__":
    print()
