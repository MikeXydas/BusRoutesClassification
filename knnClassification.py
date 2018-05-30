from fastdtw import fastdtw
from ast import literal_eval
from haversine import haversine
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from pandas import DataFrame

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

    #With dtw find distance of the Test from each trainRoute
    def createDistances(self, Test):
        distances = list()
        testCoords = np.array(Test)
        #sortedDistances = list()
        for whichTrain in xrange(len(self.X)):
            #print self.X[whichTrain]
            trajs2 = self.X[whichTrain]
            t2, lon2, lats2 = zip(*trajs2)
            coords2 = zip(lats2, lon2)
            trainCoords = np.array(coords2)
            distance, path = fastdtw(testCoords, trainCoords, dist=haversine)
            distances.append(distance)

        distRoute = zip(distances, self.y)
        sortedDistances = sorted(distRoute)
        topK = sortedDistances[0: self.numb_neighbors]

        #Perform majority voting
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

        #return the route that hade the most votes
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
        return results


trainSet = pd.read_csv('train_set.csv', converters={"Trajectory": literal_eval})
testSet = pd.read_csv('test_set_a1.csv', converters={"Trajectory": literal_eval})
trainSet = trainSet[0:600]

allTrajs = list()

knn = KNN_Classifier()

#Classification of test sets
print " >>> Test set classification begins..."
knn.fit(trainSet['Trajectory'], trainSet['journeyPatternId'])
testResults = knn.predict(testSet['Trajectory'])
listResults = list()

for whichRes in xrange(len(testResults)):
    listResults.append([whichRes, testResults[whichRes]])

header = ["Test_Trip_ID", "Pattern_JourneyPatternID"]
df2 = DataFrame(listResults, columns=header)

df2.to_csv('testSet_JourneyPatternIDs.csv',  header=True, sep='\t', index=False)

print " >>> Cross-validation begins..."
#Kfold cross-validation
kf = KFold(n_splits=10, random_state=None, shuffle=True)

Xtrajs = list()
Xjourneys = list()
for whichTraj, whichJourneyId in zip(trainSet["Trajectory"], trainSet['journeyPatternId']):
    Xtrajs.append(whichTraj)
    Xjourneys.append(whichJourneyId)

Xtrajs = np.array(Xtrajs)
Xjourneys = np.array(Xjourneys)

totalAcc = 0
whichFold = 0
for train_index, test_index in kf.split(Xtrajs):
    X_train, X_test = Xtrajs[train_index], Xtrajs[test_index]
    y_train, y_test = Xjourneys[train_index], Xjourneys[test_index]
    knn.fit(X_train, y_train)
    y_predicted = knn.predict(X_test)
    print "Accuracy of fold ", whichFold, ": ", accuracy_score(y_test, y_predicted)
    whichFold += 1

print " >>> Mean accuracy was: ", float(totalAcc) / 10








