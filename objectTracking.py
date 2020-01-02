# import the necessary packages
from imutils.video import VideoStream
from imagefiltering import imageFilter
import imutils
import time
import cv2

class ObjectTracker(object):
	def __init__(self, amountofIterations = 10,minArea = 10000,maxArea = 40000,fps = 10, *args, **kwargs):
		self.amountofIterations = amountofIterations
		self.minArea = minArea
		self.maxArea = maxArea
		self.fps = fps
		self.vs = VideoStream(src=0).start()
		# initialize the first frame in the video stream
		self.firstFrame = None
		self.d = None
		self.previousFrame = None
		self.objectFound = None
		self.framefilteredprevious = None
		self.imageFilter = imageFilter()

	def __del__(self):
		print('object del')
		#self.vs.release()
		cv2.destroyAllWindows()

	def getD(self):
    		return self.d

	def checkForImage(self):
    	
		self.objectFound = None 
	#time.sleep(1/self.fps)
	# grab the current frame and initialize the occupied/unoccupied
		frame = self.vs.read()
    # Make sure we have a frame to use. Otherwise break
		if frame is None: 
			print('frame was none')
			return
	# resize the frame, convert it to grayscale, and blur it
		frame = imutils.resize(frame, width=500)
		self.testframe = frame
		framefiltered = self.imageFilter.GMGfilter(frame)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (31, 31), 0)

	# if the first frame is None, initialize it
		if self.firstFrame is None:
			self.firstFrame = gray
			self.previousFrame = gray
			self.framefilteredprevious = gray
		
	# compute the absolute difference between the current frame and
	# first frame
		frameDelta = cv2.absdiff(gray, self.previousFrame)
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
			self.objectFound = frame[y:y+h, x:x+w]
			cv2.putText(frame,'contourArea : ' + str(cv2.contourArea(c)), 
    			(x,y), 
    			cv2.FONT_HERSHEY_SIMPLEX, 
    			3/4,
    			(255,0,0),
    			1)
		self.previousFrame = gray
		self.framefilteredprevious = framefiltered
		self.d = [frame,framefiltered, self.objectFound]
