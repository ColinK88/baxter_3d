#!/usr/bin/env python

import cv2
import numpy as np
import roslib
import rospy
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header, String
from sensor_msgs.msg import Image, CameraInfo, PointCloud2 
import sensor_msgs.point_cloud2 as pc2
from ug_stereomatcher.msg import CamerasSync
import time
from capture import * # TODO decouple this from ROS and have capture and ros working together in main only

__bridge = CvBridge()
__proc = None
__pubAcquireImages = None
__pubImageLeft = None
__pubImageRight = None
__imageQueue = []
__lastPointCloud = None


""" depends...

'header', 'height', 'width', 'encoding', 'is_bigendian', 'step', 'data

cv_bridge
std_msgs
sensor_msgs
rospy
roslib

"""
pubImageLeft = None
pubImageRight = None
pubInfoLeft = None
pubInfoRight = None

_toggle = True

#pubRight = rospy.Publisher('imR', Image, queue_size=30)


br = CvBridge()

def initTopics():
	global pubImageLeft, pubImageRight, pubInfoLeft, pubInfoRight

	pubImageLeft = rospy.Publisher('input_left_image', Image, queue_size=30)
	pubImageRight = rospy.Publisher('input_right_image', Image, queue_size=30)
	pubInfoLeft = rospy.Publisher('camera_info_left', CameraInfo, queue_size=30)
	pubInfoRight = rospy.Publisher('camera_info_right', CameraInfo, queue_size=30)

	pubAcquire = rospy.Publisher('acquire_images', CamerasSync, queue_size=10)

	#subPointCloud = rospy.Subscriber('output_pointcloud', PointCloud2, getPointCloud)
	#subDisparity = rospy.Subscriber('output_disparityC', DiparityImage, disp)
	

def publishImages(images):

	pubLeft.publish( makeROSImage(images[0]) )
	pubRight.publish( makeROSImage(images[1]) )

def makeROSImage(image):
	#todo ensure this is correct
	ros_image = br.cv2_to_imgmsg(image)
	ros_image.header.stamp = rospy.Time.now()
	ros_image.encoding = 'rgb8'

	return ros_image

def makeROSInfo(image):
	ci = CameraInfo()

	head = Header()
	head.stamp = rospy.Time.now()
	ci.header = head


	w,h = image.shape[:2]

	ci.width = w
	ci.height = h
	ci.distortion_model = 'plumb_bob'

	return ci

	#header,width,height

def ROSPublish(cams):
	global pubImageLeft, pubImageRight, pubInfoLeft, pubInfoRight
	global toggle
	
	rate = rospy.Rate(1)

	while _toggle:
		
		if DispPublished():

			images = getFrames(cams)

			infoLeft = makeROSInfo(images[0])
			infoRight = makeROSInfo(images[1])

			imageleft = makeROSImage(images[0])
			imageRight = makeROSImage(images[1])

			pubImageLeft.publish(imageleft)
			pubInfoLeft.publish(infoLeft)

			pubImageRight.publish(imageRight)
			pubInfoRight.publish(infoRight)

			print 'New stereo images published'

		else:
			rate.sleep()	

def ToggleCapture(toggle):
	global _toggle
	_toggle = toggle

def DispPublished(): # effectively this will be used as the rate, determined by point cloud returns

	time.sleep(3)

	return True

##########


def getPointCloud(data):
	
	print 'Point cloud received.'


"""
def __extractPointCloud(data):
	iterData = pc2.read_points(data)
	points = []
	height = sqrt((data.width/float(16))*9)
	width = 16 * ( height/float(9) )
	height = int(height)
	width = int(width)
	maxDist = 0
	z = 2
	print "PointCloud data received."
	for i in range(width):
		intermediate = []
		for j in range(height):
			point = next(iterData)
			if(point[z]>maxDist):
				maxDist=point[z]
			intermediate.append(point)
		points.append(intermediate)
	
	points = np.array(points)
	points = np.swapaxes(points, 0, 1)
	print "New point cloud available"

	newPoints = []
	shape = (points.shape[0], points.shape[1], 3)
	
	for i in range(points.shape[0]):
		for j in range(points.shape[1]):
			zPoint = points[i][j][z]
			if(hotNear):
				value = (1 - (zPoint/maxDist)) * 255
			else:
				value = (zPoint/maxDist) * 255
			newPoints.append((0, int(value), 0))
	
	image = np.array(newPoints, dtype=np.uint8)
	image = np.reshape(image, shape)
	print "New Depth Map Image"

	cv2.imshow('depth map', image)

	return image


def constructDepthMapImage(hotNear=True, maxDist, points):
	z = 2
	newPoints = []
	shape = (points.shape[0], points.shape[1], 3)
	
	for i in range(points.shape[0]):
		for j in range(points.shape[1]):
			zPoint = points[i][j][z]
			if(hotNear):
				value = (1 - (zPoint/maxDist)) * 255
			else:
				value = (zPoint/maxDist) * 255
			newPoints.append((0, int(value), 0))
	
	image = np.array(newPoints, dtype=np.uint8)
	image = np.reshape(image, shape)
	print "New Depth Map Image"
	return image
"""