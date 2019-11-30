import time
from mss import mss

from playGame import playGame
from generateModels import generateFirstGeneration, generateOffspring, initializeModel

# initialize model
model = initializeModel()

# get first generation
modelList = generateFirstGeneration()

sct = mss()
generationCount = 0
time.sleep(2)
while True:
    generationCount += 1
    print(f"Generation {generationCount}")

    modelCount = 0
    for i, weightList in enumerate(modelList):
        modelCount += 1
        print(f"\tModel {modelCount}", end="\t\t")

        # play game with each model
        model.set_weights(weightList[1:])
        fitness = playGame(model, sct=sct)
        modelList[i][0] = fitness
        print(fitness)

    # generate next generation
    modelList = generateOffspring(modelList, generationCount, model)
