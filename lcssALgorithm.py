from gmplot import gmplot
from ast import literal_eval
from haversine import haversine

import pandas as pd
import time


class lcss(object):
    def __init__(self, X ,Y):
        self.X = X
        self.Y = Y


    def algorithm (self):
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

#Takes the array that lcss returns and returns the indexes of the biggest subsequence
def backtrackLcss(X,Y,resultArray):
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

    return pointslist

#Takes a list of indexes and returns the corresponding coordinates
def pointsToCoords(pointsList, coords):
    retCoords = list()
    for whichPoint in pointsList:
        retCoords.append(coords[whichPoint])
    return retCoords

#Draws the green line of the trainSet and then the longest subsequence (from the test)
def drawMap(redPointList, trainCoords, testCoords, whichTest, whichRoute):
    lats, lon = zip(*trainCoords)
    gmap = gmplot.GoogleMapPlotter(lats[0], lon[0], 11)
    gmap.plot(lats, lon, 'green', edge_width=4)


    if len(redPointList) == 1:
        redPointList = list()
    for i in xrange(len(redPointList)):
        if i == 0:
            if redPointList[i] != redPointList[i+1] - 1:
                redPointList[i] = -1
        elif i == len(redPointList) - 1:
            if redPointList[i] != redPointList[i-1] + 1:
                redPointList[i] = -1
        elif redPointList[i] != redPointList[i-1] + 1 and redPointList[i] != redPointList[i+1] - 1:
            redPointList[i] = -1

    redPointList = [x for x in redPointList if x != -1]


    redPointList.append(-1)
    redlist = list()
    redpointer = 0
    while redpointer < len(redPointList):
        if redPointList[redpointer] == -1:
            break
        elif redPointList[redpointer] + 1 == redPointList[redpointer + 1]:
            redlist.append(redPointList[redpointer])
        else:
            redlist.append(redPointList[redpointer])
            lats, lon = zip(*pointsToCoords(redlist, testCoords))
            gmap.plot(lats, lon, 'red', edge_width=4)
            redlist=list()
        redpointer += 1

    gmap.draw("A2_2htmls/route" + str(whichTest) + "/" + "predict" + str(whichRoute) + ".html")



trainSet = pd.read_csv('train_set.csv', converters={"Trajectory": literal_eval})
testSet = pd.read_csv('test_set_a2.csv', converters={"Trajectory": literal_eval})
#trainSet = trainSet[0:50]


for whichTest in xrange(0, testSet.shape[0]):
    start_time = time.time()
    finalArrays = list()
    print " <<< Test = ", whichTest, " >>>"
    trajs = testSet['Trajectory'][whichTest]
    t, lon, lats = zip(*trajs)
    coordsTest = zip(lats, lon)
    for whichTrain in xrange(trainSet.shape[0]):
        trajs = trainSet['Trajectory'][whichTrain]
        t, lon, lats = zip(*trajs)
        coordsTrain = zip(lats, lon)
        arr = lcss(coordsTrain, coordsTest)

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

    lats, lon = zip(*coordsTest)
    gmap = gmplot.GoogleMapPlotter(lats[0], lon[0], 11)
    gmap.plot(lats, lon, 'green', edge_width=4)
    gmap.draw("A2_2htmls/route" + str(whichTest) + "/" + "original" + str(whichTest) + ".html")

    count = 0
    for whichFinal in finalArrays:
        trajs = trainSet['Trajectory'][whichFinal[0]]
        t, lon, lats = zip(*trajs)
        coordsTrain = zip(lats, lon)
        matchingPoints = backtrackLcss(coordsTrain, coordsTest, whichFinal[2])
        print "     JP_ID:", trainSet['journeyPatternId'][whichFinal[0]], " | Matching points = ", whichFinal[1]
        drawMap(matchingPoints, coordsTrain, coordsTest, whichTest, 4 - count)
        count += 1
    print "Time = ", time.time() - start_time
    print ""
