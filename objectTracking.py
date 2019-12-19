# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

class ObjectTracker(object):
	def __init__(self, amountofIterations = 10,minArea = 5000,maxArea = 20000,fps = 10, *args, **kwargs):
		self.amountofIterations = amountofIterations
		self.minArea = minArea
		self.maxArea = maxArea
		self.fps = fps
		self.vs = VideoStream(src=0).start()
		# initialize the first frame in the video stream
		self.firstFrame = None
		self.testframe = self.vs.read()
		self.d = None
		self.previousFrame = None

	def __del__(self):
		print('object del')
		#self.vs.release()
		cv2.destroyAllWindows()

	def getD(self):
    		return self.d

	def checkForImage(self):
    	
		objectFound = None 
	#time.sleep(1/self.fps)
	# grab the current frame and initialize the occupied/unoccupied
	# text
		frame = self.vs.read()
    # Make sure we have a frame to use. Otherwise break
		if frame is None: 
			print('frame was none')
			return
	# resize the frame, convert it to grayscale, and blur it
		frame = imutils.resize(frame, width=500)
		self.testframe = frame
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
		if self.firstFrame is None:
			self.firstFrame = gray
			self.previousFrame = gray

	# compute the absolute difference between the current frame and
	# first frame
		frameDelta = cv2.absdiff(self.previousFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
		thresh = cv2.dilate(thresh, None, iterations= self.amountofIterations)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

	# loop over the contours
		for c in cnts:
		# if the contour is too small or too large, ignore it
			if cv2.contourArea(c) < self.minArea or cv2.contourArea(c) > self.maxArea:
				print(cv2.contourArea(c))
				continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			objectFound = frame[y:y+h, x:x+w]
			cv2.putText(frame,'contourArea : ' + str(cv2.contourArea(c)), 
    			(x,y), 
    			cv2.FONT_HERSHEY_SIMPLEX, 
    			1/2,
    			(255,0,0),
    			1)
		self.previousFrame = gray
		print('d updated')
		self.d = [frame, objectFound]
