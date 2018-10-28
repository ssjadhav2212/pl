import csv
import random
import math


def loadCSV(filename):
	lines = csv.reader(open(filename, "rt"))
	dataset = list(lines)
	for i in range(1, len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset


def splitDataset(dataset, splitratio):
	trainSize = int(len(dataset) * splitratio)
	trainSet = []
	copy = list(dataset)
	while (len(trainSet) < trainSize):
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]


def separateByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in separated):
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated


def mean(numbers):
	sum = 0.0
	for i in range(len(numbers)-1):
		print(type(numbers[i]))
		sum = sum + numbers[i]

	return sum / float(len(numbers))


def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(float(x) - avg, 2) for x in numbers]) / float(len(numbers) - 1)
	return math.sqrt(variance)


# summarize() function

def summarize(dataset):
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries


def summarize(dataset):
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries


def summarizeByClass(dataset):
	separated = separateByClass(dataset)
	summaries = {}
	for classValue, instances in separated.items():
		summaries[classValue] = summarize(instances)
	return summaries


def calculateProbability(x, mean, stdev):
	print(type(x))
	exponent = math.exp(-(math.pow(float(x) - mean, 2) / (2 * math.pow(stdev, 2))))
	return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent


# ode for the calculateClassProbabilities() function

def calculateClassProbabilities(summaries, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.items():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities


def calculateClassProbabilities(summaries, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.items():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities


def predict(summaries, inputVector):
	probabilities = calculateClassProbabilities(summaries, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.iteritems():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel


def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
		predictions.append(result)
	return predictions


def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct / float(len(testSet))) * 100.0


# dataset = loadCSV(filename)


def main():
	filename = 'C:\\Users\\Amruta K\\Downloads\\diabetes.csv'
	splitRatio = 0.67
	dataset = loadCSV(filename)

	trainingSet, testSet = splitDataset(dataset, splitRatio)
	# print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainingSet), len(testSet))
	# prepare model
	summaries = summarizeByClass(trainingSet)
	# test model
	predictions = getPredictions(summaries, testSet)
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: {0}%').format(accuracy)


main()
