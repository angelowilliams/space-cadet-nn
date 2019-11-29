import numpy as np
import cv2 as cv
from mss import mss
from skimage.measure import compare_ssim
import imutils


def getContours(lastFrame, grayFrame):
    (score, diff) = compare_ssim(lastFrame, grayFrame, full=True)
    diff = (diff * 255).astype('uint8')

    thresh = cv.threshold(diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    return cnts


def getBallContours(lastBallFrame, frame, hsv):
    # Applies a mask to the HSV image to find the pinball
    lower = (0, 0, 140)
    upper = (5, 5, 145)
    mask = cv.inRange(hsv, lower, upper)
    result = cv.bitwise_and(frame, frame, mask=mask)
    gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)

    return gray, getContours(lastBallFrame, gray)


def getFrames(lastFrame, lastBallFrame, firstFrame=False, sct=mss()):
    if firstFrame:
        output = 255 * np.ones((402, 384, 3), dtype=np.uint8)
        output = cv.cvtColor(output, cv.COLOR_BGR2GRAY)
        lastFrame = output
        lastBallFrame = output
    else:
        gameMonitor = {'top': 375, 'left': 660, 'width': 384, 'height': 402}

        # Grabs the pinball screen
        frame = np.array(sct.grab(gameMonitor))

        #frame = cv.resize(frame, (128, 134))
        # Convert the frame to both grayscale and HSV
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        lastBallFrame, ballCnts = getBallContours(lastBallFrame, frame, hsv)

        output = 255 * np.ones((len(frame), len(frame[0]), 3), dtype=np.uint8)

        cnts = getContours(lastFrame, gray)
        lastFrame = gray

        for c in cnts:
        	# compute the bounding box of the contour and then draw the
        	# bounding box on both input images to represent where the two
        	# images differ
        	(x, y, w, h) = cv.boundingRect(c)
        	#cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        	cv.rectangle(output, (x + 2, y + 2), (x + w - 2, y + h - 2), (155, 155, 155), -1)
        for c in ballCnts:
        	(x, y, w, h) = cv.boundingRect(c)
        	#cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        	cv.rectangle(output, (x + 2, y + 2), (x + w - 2, y + h - 2), (0, 0, 0), -1)

        output = cv.cvtColor(output, cv.COLOR_BGR2GRAY)

    return output, lastFrame, lastBallFrame
