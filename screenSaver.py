import os
from datetime import datetime

class ScreenSaver(object):
    def switchScreenSaver(self,turnOff, overRule = False):
        if overRule is True: 
            os.system("DISPLAY=:0 xset dpms force on")
        else: 
            if turnOff is True:
                print('off')
                os.system("DISPLAY=:0 xset dpms force off")
            else:
                print('on')

                os.system("DISPLAY=:0 xset dpms force on")