import os
from datetime import datetime

class ScreenSaver(object):
    def __init__(self):
        self.num = 0
    def switchScreenSaver(self,turnOff):
        self.num +=1
        if turnOff is False:
            print('off' + str(self.num))
            self.num = 0
            #os.system("DISPLAY=:0 xset dpms force off")
        elif self.num > 10:
            self.num = 0
            print('on' + str(self.num))
            #os.system("DISPLAY=:0 xset dpms force on")