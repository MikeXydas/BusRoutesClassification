from gmplot import gmplot
from sklearn import preprocessing
import pandas as pd

from ast import literal_eval
import random

trainSet= pd.read_csv('train_set.csv', converters={"Trajectory": literal_eval})

le = preprocessing.LabelEncoder()
le.fit(trainSet["journeyPatternId"])
routeLabels = le.transform(trainSet["journeyPatternId"])

routes = list()
x = 0
while (x < 5):
    k = random.randint(0, trainSet.shape[0] - 1)
    uniqueRoute = 1
    for j in routes:
        if j == routeLabels[k]:
            uniqueRoute = 0

    if uniqueRoute == 1:
        trajs = trainSet['Trajectory'][k]
        time, lon, lats = zip(*trajs)
        gmap = gmplot.GoogleMapPlotter(lats[0], lon[0], 13)
        gmap.plot(lats, lon, 'green', edge_width=5)
        gmap.draw("A1htmls/randomRoute" + str(x) + ".html")
        x += 1
        routes.append(routeLabels[k])
