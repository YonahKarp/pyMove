# import the necessary packages
from threading import Thread
import cv2

class WebcamStream:
    def __init__(self, src=0):
        self.stopped = False

        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 0)

        (self.grabbed, self.frame) = self.stream.read()

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped: return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True