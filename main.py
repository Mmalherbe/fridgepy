import advancedtimer
from objectTracking import ObjectTracker
from imageclassifier.Labelfinder import imageClassifier
from time import sleep
import cv2
import threading
import kivy
kivy.require('1.0.7')
from kivy.app import App

# Image checking interval in seconds

class MainApp(App):
    kv_directory = 'kivy-gui'

class controller(object):
    def __init__(self):
        self.imageInterval = 0.1
        self.imageTimer = None
        self.loopTimer = None
        self.frame = None
        self.objectFound =  None
        self.objectTracker = ObjectTracker()
        self.d = None
        self.productFinder = imageClassifier()
        self.thImage = threading.Thread(target= self.startImageTimer)
        self.thImage.start()
        self.checkForImage()
        
        
    def startMainLoopTimer(self):
        if(threading.currentThread() == threading.main_thread()):
            self.loopTimer = advancedtimer.RepeatedTimer(1,self.mainLoop)
            self.loopTimer.start()
        else:
            print('not main')
    

    def startImageTimer(self):
        self.imageTimer = advancedtimer.RepeatedTimer(self.imageInterval,self.checkForImage)
        self.imageTimer.start()
    

    def stop(self):
        self.imageTimer.stop()
        self.objectTracker.stop()
        self.loopTimer.stop()
    

    def checkForImage(self):

        self.objectTracker.checkForImage()
        

    def mainLoop(self):
        MainApp().run()
        while(True):
            return
            if(threading.currentThread() is  threading.main_thread()):
                imgs = self.objectTracker.getD()
                k = cv2.waitKey(1) & 0xFF
                # press 'q' to exit
                if k == ord('q'):
                    self.stop()
                    return
                if imgs is not None:
                    if imgs[0] is not None:
                        cv2.imshow('frame',imgs[0])
                    #if imgs[1] is not None:
                       # cv2.imshow('frame filtered', imgs[1])
                       
                    if imgs[2] is not None:
                        cv2.imshow('object found', imgs[2])
                        labelprobs=self.productFinder.checkForKnownLabel(imgs[2])
                        if len (labelprobs) > 0: 
                            print(labelprobs)
                            
                else:
                    print('imgs was none')

            else:
                print('Not Main Thread')

            sleep(0.1)



control = controller()
control.mainLoop()
