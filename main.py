import advancedtimer
from objectTracking import ObjectTracker
from imageclassifier.Labelfinder import imageClassifier
from gui.guiwindow import GuiWindow
from screenSaver import ScreenSaver
from time import sleep
import cv2
import os
import threading
from datastorage.datacontroller import dbController
import PIL.Image
import tensorflow as tf # TF2 required
class controller(object):
    def __init__(self):
        with open('/sys/firmware/devicetree/base/model', 'r') as f:
            isRaspberry = "raspberry" in f
        self.imageInterval = 0.5
        self.dbController = dbController()
        self.imageTimer = None
        self.loopTimer = None
        self.screenSaveTimer = None
        self.screenSaver = ScreenSaver()
        self.frame = None
        self.objectFound =  None
        self.mayLookForProduct = True
        self.objectTracker = ObjectTracker(rpi = isRaspberry)
        self.d = None
        self.window = GuiWindow(self)
        self.productFinder = imageClassifier()
        self.thImage = threading.Thread(target= self.startImageTimer)
        self.thMain = threading.Thread(target=self.startMainLoopTimer)
        self.thScreensave = threading.Thread(target = self.startScreensaveTimer)
        self.thMain.start()
        self.thImage.start()
        self.checkForImage()
        self.window.setEvents()
        self.movementDetected = False
        self.window.run() # make sure I'm last 

    def screenSaveCheck(self,forceOn):
        if forceOn:
            self.screenSaver.switchScreenSaver(tunOff=False)
            self.screenSaveTimer.stop()
            self.screenSaveTimer.start()

        elif self.movementDetected is False :
            self.screenSaver.switchScreenSaver(turnOff=True)


    def startScreensaveTimer(self):
        self.screenSaveTimer = advancedtimer.RepeatedTimer(10,self.screenSaveCheck)
        self.screenSaveTimer.start()
        
    def startMainLoopTimer(self):
        self.loopTimer = advancedtimer.RepeatedTimer(0.2,self.mainLoop)
        self.loopTimer.start()

    def startImageTimer(self):
        self.movementDetected = self.objectTracker.movementFound
        self.imageTimer = advancedtimer.RepeatedTimer(self.imageInterval,self.checkForImage)
        self.imageTimer.start()
    

    def stop(self):
        self.imageTimer.stop()
        self.thImage._stop()
        self.thScreensave._stop()
        self.loopTimer.stop()
        self.window.stop()
        os._exit(1)
        exit()
    def checkForImage(self):
        self.objectTracker.checkForImage()
    def getFullStock(self):
        return self.dbController.getAll()

    def ProductChange(self,productName,amount):
        self.dbController.dataBase.set(productName,amount)
    def mainLoop(self):
                if self.mayLookForProduct is False:
                    return
                imgs = self.objectTracker.getD()
                if imgs is not None:
                    if imgs[0] is not None:
                       self.window.updateUI(imgs[0])
                    #if imgs[1] is not None:
                       # cv2.imshow('frame filtered', imgs[1])
                    if imgs[2] is not None:
                        #cv2.imshow('object found', imgs[2])
                        labelprobs=self.productFinder.checkForKnownLabel(imgs[2])
                        if labelprobs is None:
                            return
                        if len (labelprobs) > 0: 
                            self.mayLookForProduct  = False
                            productfound = list(labelprobs.keys())[0]
                            self.window.showFound(productfound,self.dbController.getStock(productfound))




control = controller()
control.mainLoop()
