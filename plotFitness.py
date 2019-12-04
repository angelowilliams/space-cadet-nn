import matplotlib.pyplot as plt

averageFitness = []
bestFitness = []
with open('models/fitness.txt', 'r') as fp:
    for line in fp:
        if line.startswith('Average Fitness'):
            averageFitness.append(float(line.split(': ')[1]))
        if line.startswith('Best Fitness'):
            bestFitness.append(float(line.split(': ')[1]))

for i in range(len(bestFitness)):
    plt.scatter(i, bestFitness[i], c='r')

plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Best Fitness by Generation')
plt.show()
