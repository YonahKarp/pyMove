import cv2
import numpy as np
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