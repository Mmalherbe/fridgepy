# import the necessary packages
import imutils
import time
import cv2

class imageFilter(object):
    def __init__(self, initializationFrames = 10, decisionThreshold = .8):
        self.initializationFrames = initializationFrames
        self.decisionThreshold = decisionThreshold
        self.gmgMask = None
        self.gmgSubtractor = cv2.bgsegm.createBackgroundSubtractorGMG(self.initializationFrames, self.decisionThreshold)
        self.tempFrame = None

    def GMGfilter(self,frame):
        if frame is not None:
            self.tempFrame = frame

        self.gmgMask = self.gmgSubtractor.apply(self.tempFrame)
        self.gmgMask = cv2.morphologyEx(self.gmgMask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
        return self.gmgMask


