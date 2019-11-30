import pytesseract
import cv2 as cv
from mss import mss
import numpy as np
import time
from pynput.keyboard import Key, Controller

from getFrames import getFrames

def playGame(model, sct=mss()):
    keyboard = Controller()
    frameCount = 0
    lastBallFrame, x, y, v_x, v_y = getFrames(None, 0, 0, firstFrame=True, sct=sct)
    scoreMonitor = {'top': 560, 'left': 1097, 'width': 145, 'height': 25}
    deploymentMonitor = {'top': 655, 'left': 1055, 'width': 150, 'height': 62}
    lastScore = -1
    leftTimer = rightTimer = 0
    inputCount = 0

    keyboard.press(Key.f2)
    keyboard.release(Key.f2)
    time.sleep(8)
    keyboard.press(Key.space)
    time.sleep(3)
    keyboard.release(Key.space)
    time.sleep(3)

    while True:
        t1 = time.time()

        lastBallFrame, x, y, v_x, v_y = getFrames(lastBallFrame, x, y, sct=sct)

        if frameCount % 150 == 0:
            score = np.array(sct.grab(scoreMonitor))
            score = pytesseract.image_to_string(score)
            if lastScore == score:
                break
            lastScore = score

        left, right = model.predict(np.array([x, y, v_x, v_y]).reshape(1,4))[0]

        if left > 0.5:
            keyboard.press('z')
            leftTimer = 5
            inputCount += 1
        if right > 0.5:
            keyboard.press('/')
            rightTimer = 5
            inputCount += 1
        if leftTimer == 0:
            keyboard.release('z')
        if rightTimer == 0:
            keyboard.release('/')

        frameCount += 1
        leftTimer -= 1
        rightTimer -= 1

        t2 = time.time()
        if (t2 - t1) <= 0.033:
            time.sleep(0.033 - (t2 - t1))

    keyboard.release('z')
    keyboard.release('/')

    try:
        return int(score) - (inputCount * 10)
    except:
        return 0
