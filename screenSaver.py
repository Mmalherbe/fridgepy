import os
from datetime import datetime

class ScreenSaver(object):
    def switchScreenSaver(self,turnOff):
        if turnOff is True:
            os.system("DISPLAY=:0 xset dpms force off")
        else:
            os.system("DISPLAY=:0 xset dpms force on")