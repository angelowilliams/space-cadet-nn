import time
from mss import mss

from playGame import playGame
from generateModels import generateFirstGeneration, generateOffspring, initializeModel, loadFirstGeneration

# initialize model
model = initializeModel()

# get first generation
weight_list = loadFirstGeneration(29)[1]
model.set_weights(weight_list[1:])
sct = mss()

time.sleep(2)
playGame(model, sct=sct)
