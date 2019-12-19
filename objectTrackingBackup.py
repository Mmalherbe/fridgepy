# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

class ObjectTracker(object):
	def __init__(self, function, *args, **kwargs):
		amountofIterations = 10
		minArea = 5000
		fps = 10
		vs = VideoStream(src=0).start()
		#time.sleep(2.0)
		# initialize the first frame in the video stream
		firstFrame = None

#variables

# if the video argument is None, then we are reading from webcam
#if args.get("video", None) is None:




# loop over the frames of the video
	def checkForImage():
    	
		time.sleep(1/fps)
	# grab the current frame and initialize the occupied/unoccupied
	# text
        frame = vs.read()
    # Make sure we have a frame to use. Otherwise break
        if frame is None: 
            return

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		previousFrame = gray
	else:
    		return


	# compute the absolute difference between the current frame and
	# first frame


	frameDelta = cv2.absdiff(previousFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations= amountofIterations)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < minArea:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		objectFound = frame[y:y+h, x:x+w]
		cv2.imshow('crop',objectFound)
	# show the frame and record if the user presses a key
	#cv2.imshow("Security Feed", frame) <- uncomment to see image
	previousFrame = gray
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
	#key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
	#if key == ord("q"):
	#	return
	return { frame, objectFound}
# cleanup the camera and close any open windows
	vs.release()
	cv2.destroyAllWindows()
