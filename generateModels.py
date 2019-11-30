from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import random
import os

def initializeModel():
    model = Sequential()
    model.add(Dense(8, activation='relu', input_shape=(4,)))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(2, activation='sigmoid'))

    model.compile(loss='mse',
              optimizer='adam')

    return model

def generateFirstGeneration():
    model = initializeModel()
    weights = model.get_weights()

    amount = 20
    min = -1
    max = 1

    modelList = []
    for _ in range(amount):
        arr1 = [0]
        for i in range(len(weights)):
            arr2 = []
            for j in range(len(weights[i])):
                arr2.append(weights[i][j] + (min + (random.random() * (max - min))))
            arr1.append(np.array(arr2))
        modelList.append(np.array(arr1))

    return modelList


def generateOffspring(parentModels, generationNum, model):
    amountPerGeneration = 20
    mutationRate = 0.1
    mutationAmount = 1

    parentModels = sorted(parentModels, key=lambda x: x[0], reverse=True)
    model1 = parentModels[0]
    model2 = parentModels[1]
    model3 = parentModels[2]
    model.set_weights(model1[1:])
    model.save(os.path.join("models", f"{generationNum}_1"))
    model.set_weights(model2[1:])
    model.save(os.path.join("models", f"{generationNum}_2"))
    model.set_weights(model3[1:])
    model.save(os.path.join("models", f"{generationNum}_3"))
    totalScore = model1[0] + model2[0] + model3[0]
    model1CrossoverProb = model1[0] / totalScore
    model2CrossoverProb = model2[0] / totalScore

    modelList = []
    for _ in range(amountPerGeneration):
        arr1 = [0]
        for i in range(1, len(model1)):
            arr2 = []
            for j in range(len(model1[i])):
                rand1 = random.random()
                rand2 = random.random()
                if rand1 > (1 - model1CrossoverProb):
                    arr2.append(model1[i][j])
                elif rand1 > (1 - model1CrossoverProb - model2CrossoverProb):
                    arr2.append(model2[i][j])
                else:
                    arr2.append(model3[i][j])
                if rand2 < mutationRate:
                    arr2[-1] += (-mutationAmount + (random.random() * 2 * mutationAmount))
            arr1.append(np.array(arr2))
        modelList.append(np.array(arr1))

    return modelList
