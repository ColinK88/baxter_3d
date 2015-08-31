#!/usr/bin/env python

import cv2
import numpy as np

__width = 0
__height = 0
__mode = 0


"""
Major TODO: fix __height, __width assignment so that 
setResolution changes these variables globally, 
instead of getting image.shape locally each time it is needed...
"""

def getFrames(cams):

	return (getFrame(cams[0]), getFrame(cams[1]) )


def getFrame(cam): # TODO return ret, to test return frames and exit properly
	try:
		ret, frame = cam.read()
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		return frame
	except:
		return None

def getImage(cams): # TODO make this conditional set the return instead of the image...? generally refactor this.
	
	mode = getCaptureMode()
	
	if mode == 0:
		image = getAnaglyph(getFrames(cams))

	elif mode == 1:
		ret, frame = cams[1].read()
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		image = getRed(frame)

	elif mode == 2:
		ret, frame = cams[0].read()
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		image = getGreenBlue(frame)

	elif mode == 3:
		image = getSideBySide(getFrames(cams))

		

	return image

def setCaptureMode(mode):
	global __mode

	__mode = mode
	print mode

def getCaptureMode():
	global __mode

	return __mode

def getRed(image):
	
	__height, __width = image.shape[:2]

	red = np.zeros((__height, __width, 3), np.uint8)
	if image is not None:
		red[:,:,2] = image[:,:,2]
	return red

def getGreenBlue(image):

	__height, __width = image.shape[:2]

	greenBlue = np.zeros((__height, __width, 3), np.uint8)
	if image is not None:
		greenBlue[:,:,:2] = image[:,:,:2]
	return  greenBlue

def __combineImages(image1, image2):
	distance = 0

	width = image1.shape[1]
	height = image2.shape[0]
	totalWidth = width + distance

	image = np.zeros((height, totalWidth, 3), np.uint8)
	image[:, :width, 2] = image1[:, :, 2]
	image[:, distance:, :2] = image2[:, :, :2]

	return image

def getAnaglyph(frames):
	image = None
	imageRed = getRed(frames[1])
	imageGreenBlue = getGreenBlue(frames[0])
	image = __combineImages(imageRed, imageGreenBlue)

	return image

def getSideBySide(frames):
	image = np.hstack((frames[0], frames[1]))
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	return image

def getCVDepthMap(frames):
	print "something"

def setResolution(resolution, cams):
		global __width, __height

		cams[0].set(3, resolution[0])
		cams[0].set(4, resolution[1])

		cams[1].set(3, resolution[0])
		cams[1].set(4, resolution[1])

		__width = cams[0].get(3)
		__height = cams[0].get(4)

		print "setRes: "+str(__width)+" "+str (__height)


def getHeight():
	return __height
	
def getWidth():
	return __width

"""

def saveImage(cams):

	imageL = getFrame(cams[0])
	imageR = getFrame(cams[1])

	height, width = imageL.shape[:2]

	imageL = cv2.cvtColor(imageL, cv2.COLOR_BGR2RGB)
	imageR = cv2.cvtColor(imageR, cv2.COLOR_BGR2RGB)

	cv2.imwrite('imageL.jpg', imageL)
	cv2.imwrite('imageR.jpg', imageR)
"""
