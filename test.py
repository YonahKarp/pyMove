import cv2
import time
import os
import subprocess



from WebcamStream import WebcamStream





if __name__ == "__main__":

    cap = WebcamStream().start()
    pid = os.getpid()

    subprocess.call(f"sudo renice -15 {pid}", shell=True)

    frameNum = 0
    while(True):
        frameNum += 1
        frame = cap.read()

        # if frame[0,0,0] < 30 and frame[-1,-1,-1] < 30:
        #     print(f'covered: {frameNum}')
        start = time.time()
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

        if(frameNum % 3 == 0):
            print(time.time() - start)


