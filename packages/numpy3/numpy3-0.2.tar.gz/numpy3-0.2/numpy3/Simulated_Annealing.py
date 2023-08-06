# PYTHON CODE for the above approach
import random
import math


class Solution:
	def __init__(self, CVRMSE, configuration):
		self.CVRMSE = CVRMSE
		self.config = configuration


T = 1
Tmin = 0.0001
alpha = 0.9
numIterations = 100


def genRandSol():
	# Instantiating for the sake of compilation
	a = [1, 2, 3, 4, 5]
	return Solution(-1.0, a)


def neighbor(currentSol):
	return currentSol


def cost(inputConfiguration):
	return -1.0

# Mapping from [0, M*N] --> [0,M]x[0,N]


def indexToPoints(index):
	points = [index % M, index//M]
	return points


M = 5
N = 5
sourceArray = [['X' for i in range(N)] for j in range(M)]
min = Solution(float('inf'), None)
currentSol = genRandSol()

while T > Tmin:
	for i in range(numIterations):
		# Reassigns global minimum accordingly
		if currentSol.CVRMSE < min.CVRMSE:
			min = currentSol
		newSol = neighbor(currentSol)
		ap = math.exp((currentSol.CVRMSE - newSol.CVRMSE)/T)
		if ap > random.uniform(0, 1):
			currentSol = newSol
	T *= alpha # Decreases T, cooling phase

# Returns minimum value based on optimization
print(min.CVRMSE, "\n\n")

for i in range(M):
	for j in range(N):
		sourceArray[i][j] = "X"

# Displays
for obj in min.config:
	coord = indexToPoints(obj)
	sourceArray[coord[0]][coord[1]] = "-"

# Displays optimal location
for i in range(M):
	row = ""
	for j in range(N):
		row += sourceArray[i][j] + " "
	print(row)



# import random
# import math
# def objFunc(x):
#     return math.sin(x)-math.cos(2*x)
# def simulatedAnnealing(x, maxItr, T):
#     fx = objFunc(x)
#     Tmin = 0.0001
#     for _ in range(maxItr):
#         alpha = 0.99
#         T = T*alpha
#         dx = (random.random()*2-1)*T
#         next_x = x+dx
#         next_fx = objFunc(next_x)
#         if next_fx > fx or random.random() < math.exp((next_fx-fx)/T):
#             x = next_x
#             fx = next_fx
#         if T < Tmin:
#             break
#     return x
# x=1
# maxIter = 1000 
# T = 1.0
# res = simulatedAnnealing(x, maxIter, T)
# # Print the results
# print(f'Point found: {res}\nf(x): {objFunc(res)}')