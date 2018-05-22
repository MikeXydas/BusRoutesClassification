from gmplot import gmplot
from sklearn import preprocessing
from fastdtw import fastdtw
from ast import literal_eval
from haversine import haversine
import time

import pandas as pd
import numpy as np

import random

trainSet = pd.read_csv('train_set.csv', converters={"Trajectory": literal_eval})
testSet = pd.read_csv('test_set_a1.csv', converters={"Trajectory": literal_eval})

#trainSet = trainSet[0 : 20]
#le = preprocessing.LabelEncoder()
#le.fit(trainSet["journeyPatternId"])
#routeLabels = le.transform(trainSet["journeyPatternId"])

for whichTest in xrange(0, testSet.shape[0]):
    distances = list()
    trajs = trainSet['Trajectory'][whichTest]
    t, lon, lats = zip(*trajs)
    coords = zip(lats, lon)
    testCoords = np.array(coords)
    gmap = gmplot.GoogleMapPlotter(lats[0], lon[0], 11)
    gmap.plot(lats, lon, 'green', edge_width=5)
    gmap.draw("A2_1htmls/route" + str(whichTest) + "/" + "original" + str(whichTest) + ".html")
    start_time = time.time()
    for whichTrain in xrange(trainSet.shape[0] - 1):
        trajs2 = trainSet['Trajectory'][whichTrain]
        t2, lon2, lats2 = zip(*trajs2)
        coords2 = zip(lats2, lon2)
        trainCoords = np.array(coords2)
        distance, path = fastdtw(testCoords, trainCoords, dist=haversine)
        distances.append([distance, whichTrain])

    sortedDistances = sorted(distances)

    print "Which Test = ", whichTest," Time = ", time.time() - start_time
    for whichRoute in xrange(5):
        print "        Route = ", trainSet['journeyPatternId'][sortedDistances[whichRoute][1]], " Distance = ", sortedDistances[whichRoute][0]
        trajs = trainSet['Trajectory'][sortedDistances[whichRoute][1]]
        t, lon, lats = zip(*trajs)
        coords = zip(lats, lon)
        gmap = gmplot.GoogleMapPlotter(lats[0], lon[0], 11)
        gmap.plot(lats, lon, 'green', edge_width=5)
        gmap.draw("A2_1htmls/route" + str(whichTest) + "/" + "predict"+str(whichRoute) + ".html")
    print ""


'''trajs = trainSet['Trajectory'][5]
time, lon, lats = zip(*trajs)
coords = zip(lats, lon)

x = np.array(coords)

trajs2 = testSet['Trajectory'][4]
time2, lon2, lats2 = zip(*trajs2)
coords2 = zip(lats2, lon2)

y = np.array(coords2)

distance, path= fastdtw(x, y, dist=haversine)

print distance'''


