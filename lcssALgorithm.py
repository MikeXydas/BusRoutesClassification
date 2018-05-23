from sklearn import preprocessing
from fastdtw import fastdtw
from ast import literal_eval
from haversine import haversine
import time

import pandas as pd
import numpy as np


class lcss(object):
    def __init__(self, X ,Y):
        self.X = X
        self.Y = Y


    def algorithm (self):
        #print len(self.X)
        arr = list()
        for i in xrange(0, len(self.X) + 1):
            arr.append(list())
            for j in xrange(0, len(self.Y) + 1):
                arr[i].append(0)

        for i in xrange(1, len(self.X) + 1):
            for j in xrange(1, len(self.Y) + 1):
                if haversine(self.X[i - 1], self.Y[j - 1]) < 0.2:
                    arr[i][j]=arr[i-1][j-1] + 1
                else:
                    arr[i][j] = max(arr[i][j-1], arr[i-1][j])
        return arr

def printLcss(X,Y,resultArray):
    pointslist=list()
    i = len(X)
    j = len(Y)
    while i > 0 and j > 0:
        #print i, " ", j, " LenX = ", len(X), "LenY = ", len(Y), "ResLines = ", len(resultArray), "LenY = ", len(resultArray[0])
        if haversine(X[i - 1], Y[j - 1]) < 0.2:
            pointslist.insert(0, j-1)
            i -= 1
            j -= 1
        elif resultArray[i-1][j] > resultArray[i][j-1]:
            i -= 1
        else:
            j -= 1

    print pointslist

#def drawMap(redPointList, allPoints):


trainSet = pd.read_csv('train_set.csv', converters={"Trajectory": literal_eval})
testSet = pd.read_csv('test_set_a2.csv', converters={"Trajectory": literal_eval})
trainSet = trainSet[0:50]


for whichTest in xrange(0, testSet.shape[0]):
    finalArrays = list()
    print ""
    print " <<< test = ", whichTest, " >>>"
    trajs = testSet['Trajectory'][whichTest]
    t, lon, lats = zip(*trajs)
    coordsTest = zip(lats, lon)
    #testCoords = np.array(coords)
    for whichTrain in xrange(trainSet.shape[0]):
        trajs = trainSet['Trajectory'][whichTrain]
        t, lon, lats = zip(*trajs)
        coordsTrain = zip(lats, lon)
        arr = lcss(coordsTest, coordsTrain)

        result = arr.algorithm()
        biggestSubseq = result[len(result) - 1][len(result[0]) - 1]
        if len(finalArrays) < 5:
            finalArrays.append([whichTrain, biggestSubseq, result])
        elif finalArrays[0][1] < biggestSubseq:
            finalArrays[0][0] = whichTrain
            finalArrays[0][1] = biggestSubseq
            finalArrays[0][2] = result
        else:
            continue

        finalArrays = sorted(finalArrays, key=lambda x: int(x[1]))


    for whichFinal in finalArrays:
        trajs = trainSet['Trajectory'][whichFinal[0]]
        t, lon, lats = zip(*trajs)
        coordsTrain = zip(lats, lon)
        printLcss(coordsTest, coordsTrain, whichFinal[2])
