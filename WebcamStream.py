# import the necessary packages
from threading import Thread
import cv2
import time

class WebcamStream:
    def __init__(self, src=0, border=250, scale=.2):
        self.stopped = False
        self.border = border
        self.scale = scale

        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        (self.grabbed, self.frame) = self.stream.read()
        self.hasNew = True

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped: return
            # start = time.time()
            (self.grabbed, frame) = self.stream.read()
            # print(time.time() - start)

            frame = frame[:, self.border:frame.shape[1]-self.border]
            self.frame = cv2.resize(frame, (int(frame.shape[1]*self.scale), int(frame.shape[0]*self.scale)), interpolation = cv2.INTER_AREA)
            # self.hasNew = True

    def read(self):
        # while not self.hasNew:
        #     time.sleep(.001)
        # self.hasNew = False
        return self.frame

    def stop(self):
        self.stopped = True

    def __del__(self):
        self.stream.release()