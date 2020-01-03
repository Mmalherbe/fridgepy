import advancedtimer
from objectTracking import ObjectTracker
from imageclassifier.Labelfinder import imageClassifier
from gui.guiwindow import GuiWindow
from time import sleep
import cv2
import os
import threading
from datastorage.datacontroller import dbController
        
class controller(object):
    def __init__(self):
        self.imageInterval = 0.1
        self.dbController = dbController()
        self.imageTimer = None
        self.loopTimer = None
        self.frame = None
        self.objectFound =  None
        self.mayLookForProduct = True
        self.objectTracker = ObjectTracker()
        self.d = None
        self.window = GuiWindow(self)
        self.productFinder = imageClassifier()
        self.thImage = threading.Thread(target= self.startImageTimer)
        self.thMain = threading.Thread(target=self.startMainLoopTimer)
        self.thMain.start()
        self.thImage.start()
        self.checkForImage()
        self.window.setEvents()
        self.window.run() # make sure I'm last 

        
    def startMainLoopTimer(self):
        self.loopTimer = advancedtimer.RepeatedTimer(1,self.mainLoop)
        self.loopTimer.start()

    def startImageTimer(self):
        self.imageTimer = advancedtimer.RepeatedTimer(self.imageInterval,self.checkForImage)
        self.imageTimer.start()
    

    def stop(self):
        self.imageTimer.stop()
        self.thImage._stop()
        self.loopTimer.stop()
        self.window.stop()
        os._exit(1)
        exit()
    def checkForImage(self):
        self.objectTracker.checkForImage()

    def ProductChange(self,productName,amount):
        self.dbController.dataBase.set(productName,amount)
    def mainLoop(self):
                if self.mayLookForProduct is False:
                    return
                imgs = self.objectTracker.getD()
                #k = cv2.waitKey(1) & 0xFF
                # press 'q' to exit
                #if k == ord('q'):
                #    self.stop()
                #    return
                if imgs is not None:
                    if imgs[0] is not None:
                       self.window.updateUI(imgs[0])
                    #if imgs[1] is not None:
                       # cv2.imshow('frame filtered', imgs[1])
                    if imgs[2] is not None:
                        #cv2.imshow('object found', imgs[2])
                        labelprobs=self.productFinder.checkForKnownLabel(imgs[2])
                        if len (labelprobs) > 0: 
                            self.mayLookForProduct  = False
                            productfound = list(labelprobs.keys())[0]
                            self.window.showFound(productfound,self.dbController.getStock(productfound))
    sleep(0.1)




control = controller()
control.mainLoop()
