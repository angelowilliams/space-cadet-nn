import pytesseract
import cv2 as cv
from mss import mss
import numpy as np
import time

from getFrames import getFrames

def playGame(sct=mss()):
    frameCount = 0
    output, lastFrame, lastBallFrame = getFrames(None, None, firstFrame=True, sct=sct)
    scoreMonitor = {'top': 550, 'left': 1090, 'width': 150, 'height': 35}
    deploymentMonitor = {'top': 655, 'left': 1055, 'width': 150, 'height': 62}
    while True:
        output, lastFrame, lastBallFrame = getFrames(lastFrame, lastBallFrame, sct=sct)

        if frameCount % 60 == 0:
            deploymentStatus = np.array(sct.grab(deploymentMonitor))
            if pytesseract.image_to_string(deploymentStatus) == "awaiting\nDeployment":
                score = np.array(sct.grab(scoreMonitor))
                score = pytesseract.image_to_string(score)
                break

        frameCount += 1
        time.sleep(0.033)

    return score

print(playGame())
