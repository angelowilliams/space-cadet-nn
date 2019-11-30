import pytesseract
import cv2 as cv
from mss import mss
import numpy as np
import time
from pyautogui import press, keyDown, keyUp

from getFrames import getFrames
from loadModel import createModel

def playGame(model, sct=mss()):
    frameCount = 0
    lastBallFrame, x, y, v_x, v_y = getFrames(None, 0, 0, firstFrame=True, sct=sct)
    scoreMonitor = {'top': 550, 'left': 1090, 'width': 150, 'height': 35}
    deploymentMonitor = {'top': 655, 'left': 1055, 'width': 150, 'height': 62}
    leftTimer = rightTimer = 0
    while True:
        lastBallFrame, x, y, v_x, v_y = getFrames(lastBallFrame, x, y, sct=sct)

        if frameCount % 60 == 0:
            deploymentStatus = np.array(sct.grab(deploymentMonitor))
            if pytesseract.image_to_string(deploymentStatus) == "awaiting\nDeployment":
                score = np.array(sct.grab(scoreMonitor))
                score = pytesseract.image_to_string(score)
                break

        left, right = model.predict(np.array([x, y, v_x, v_y]).reshape(1,4))[0]

        print(left)
        print(right)
        print("")
        if left:
            keyDown('z')
            leftTimer = 3
        if right:
            keyDown('/')
            rightTimer = 3

        if leftTimer == 0:
            keyUp('z')
        if rightTimer == 0:
            keyUp('/')

        frameCount += 1
        leftTimer -= 1
        rightTimer -= 1
        time.sleep(0.033)

    keyUp('z')
    keyUp('/')
    return score

"""
time.sleep(7)
press('f2')
time.sleep(8)
keyDown('space')
time.sleep(3)
keyUp('space')
time.sleep(2)
"""

print(playGame(createModel()))
