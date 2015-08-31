#!/usr/bin/env python

import cv2
import time
import numpy as np
import glob

img = None
_images = []
#_mtx, _dist, _rvecs, _tvecs = None

def StartCapture(cam):

    img = cam.read()

    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    _images.append(img)

    return img

def FindPoints(cam):

    cornerCount = 0

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    while cornerCount <= 20: # maybe add a "cant find" function so this doesnt potentially hang forever
        
        ret, frame = cam.read()

        # Capture image.
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        draw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find corners on chessboard
        ret, corners = cv2.findChessboardCorners(img, (9,6) , None)
        
        # If found, add object points, image points (after refining them)
        if ret == True:

            cornerCount = cornerCount+1

            print 'Corners found: '+str(cornerCount)

            objpoints.append(objp)
        
            cv2.cornerSubPix(img,corners,(11,11),(-1,-1),criteria)

            imgpoints.append(corners)

            cv2.drawChessboardCorners(draw, (9,6), corners,ret)

            # temporary
            #cv2.imshow('corners', draw)


    w, h = img.shape[::-1]
    
    calibration = ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,(w,h),None,None)
    
    print calibration

    cv2.destroyAllWindows()

    return calibration



