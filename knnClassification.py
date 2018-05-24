from fastdtw import fastdtw
from ast import literal_eval
from haversine import haversine
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
import time

import pandas as pd
import numpy as np





class KNN_Classifier(object):
    def __init__(self, numb_neighbors=5):
        self.numb_neighbors = numb_neighbors
    def fit(self, X, y):
        self.X = X
        self.y = y
        return self

    #def return_neighbors(self, Test):
    def createDistances(self, Test):
        distances = list()
        testCoords = np.array(Test)
        #sortedDistances = list()
        print self.X[1]
        for whichTrain in xrange(len(self.X)):
            print whichTrain, " ", len(self.X)
            #print self.X[whichTrain]
            trajs2 = self.X[whichTrain]
            t2, lon2, lats2 = zip(*trajs2)
            coords2 = zip(lats2, lon2)
            trainCoords = np.array(coords2)
            distance, path = fastdtw(testCoords, trainCoords, dist=haversine)
            distances.append(distance)

        distRoute = zip(distances, self.y)
        sortedDistances = sorted(distRoute)

        topK = sortedDistances[0 : self.numb_neighbors]
        print topK
        candidates = list()
        votes = list()
        for i in topK:
            candExists = 0
            for j in candidates:
                if i[1] == j[1]:
                    candExists = 1
            if candExists == 0:
                candidates.append(i)

        for i in candidates:
            votes.append(0)

        for i in topK:
            for j in xrange(len(candidates)):
                if i[1] == candidates[j][1]:
                    votes[j] += 1

        max = -1
        maxI = -1
        for i in xrange(len(votes)):
            if votes[i] > max:
                maxI = i
                max = votes[i]

        return candidates[maxI][1]


    def predict(self, Y):
        yCoords = list()
        for whichTest in Y:
            trajs = whichTest
            t, lon, lats = zip(*trajs)
            coords = zip(lats, lon)
            yCoords.append(coords)
        results = list()
        for i in yCoords:
            results.append(self.createDistances(i))
        print results
        return results

trainSet = pd.read_csv('train_set.csv', converters={"Trajectory": literal_eval})
testSet = pd.read_csv('test_set_a1.csv', converters={"Trajectory": literal_eval})
trainSet = trainSet[0:200]


allTrajs = list()

for whichTest in xrange(0, testSet.shape[0]):
    trajs2 = testSet['Trajectory'][whichTest]
    t2, lon2, lats2 = zip(*trajs2)
    coords2 = zip(lats2, lon2)
    allTrajs.append(coords2)



knn = KNN_Classifier()

#knn.fit(trainSet['Trajectory'], trainSet['journeyPatternId'])
#knn.predict(allTrajs)
kf = KFold(n_splits=10, random_state=None, shuffle=True)

for train_index, test_index in kf.split(trainSet['Trajectory']):
    print train_index
    #for i in xrange(len(train_index)):
    X_train, X_test = trainSet['Trajectory'][train_index], trainSet['Trajectory'][test_index]
    y_train, y_test = trainSet['journeyPatternId'][train_index], trainSet['journeyPatternId'][test_index]
    knn.fit(X_train, y_train)
    y_predicted = knn.predict(X_test)
    print "Acc = ", accuracy_score(y_test, y_predicted)









