# import the necessary packages
from profiler import profile

from threading import Thread, Condition
import cv2
import time

class WebcamStream:
    def __init__(self, src=0, border=250):
        self.stopped = False
        self.border = border

        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 600)

        # self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
        # self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 300)

        (self.grabbed, self.frame) = self.stream.read()
        self.hasNew = True

        self.condition = Condition()

    def start(self):

        Thread(target=self.update, args=()).start()
        return self

    # @profile()
    def update(self,):
        while True:
            if self.stopped: return
            
            (self.grabbed, self.frame) = self.stream.read()
            with self.condition:
                self.hasNew = True
                self.condition.notify_all()

            # frame = frame[:, self.border:frame.shape[1]-self.border]
            # self.frame = cv2.resize(frame, (int(frame.shape[1]*self.scale), int(frame.shape[0]*self.scale)), interpolation = cv2.INTER_AREA)
            

    def read(self):
        if not self.hasNew:
            with self.condition:
                self.condition.wait()

        self.hasNew = False
        return self.frame

    def stop(self):
        self.stopped = True

    def __del__(self):
        self.stream.release()