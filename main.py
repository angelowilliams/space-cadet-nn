import time
from mss import mss

from playGame import playGame
from generateModels import generateFirstGeneration, generateOffspring, initializeModel, loadFirstGeneration

# initialize model
model = initializeModel()

# get first generation
#modelList = generateFirstGeneration()
modelList = loadFirstGeneration(1)

sct = mss()
generationCount = 0
time.sleep(2)
while True:
    generationCount += 1
    print(f"Generation {generationCount}")

    modelCount = 0
    bestFitness = 0
    fitnessList = []
    for i, weightList in enumerate(modelList):
        modelCount += 1

        # play game with each model
        model.set_weights(weightList[1:])
        fitness = playGame(model, sct=sct)
        if fitness > bestFitness:
            bestFitness = fitness
        fitnessList.append(fitness)
        modelList[i][0] = fitness
        print(f"\tModel {modelCount}  \t{fitness}")

    print(f"Average Fitness: {sum(fitnessList) / 20}")
    print(f"Best Fitness: {bestFitness}\n")
    # generate next generation
    modelList = generateOffspring(modelList, generationCount, model)
