# Bus Routes Classification

## Introduction

In this project the main goal is to classify bus routes to their matching line number using only their coordinates.  

### What data do we have?

We have the `train_set.csv` which has these columns:
1. `tripId`: A unique index for each bus trajectory. Care as some indexes are missing.
2. `journeyPatterId`: The line number that the trajecotry belongs
3. `Trajectory`: A list of lists. Each element of the list has a list that conists of [time, lon, lat]. The trajectories in the train_set are sorted on the time.
  
All the bus routes are in Dublin.
  
### What will we classify?

As you can see there are some `test_sets`. These test_sets have 5 routes with the Trajectory column only . Our target is to  
match these unknown lines with a journeyPatternId ("Line Number"). We will manage that thorugh 3 different  
algorithms:
- **`DTW`**: Dynamic Time Wrapping (Already sorted on time field)
- **`LCS`**: Longest Common Subsequence
- **`KNN`**: K-Nearest Neighbors

## Running

Set up the environment according to the requirements.txt. You will see that we have 4 .py. Each one will be explained int this README.
The modules will take some time to be executed (depending on your computer).

## Moudles explanation

  First of all you will see that I am using on all my modules the **haversine distance**. This formula takes into account the curve of the  
  earth, offering us more accurate distance computation.  
  More on that: https://en.wikipedia.org/wiki/Haversine_formula
    
  Also, the output .html files of the modules can be found into the corresponding direcotries.
  
### -A_1: `dataVisualisation.py`
  
  Just a module that exhibits a way of using the gmplotter (https://github.com/vgm64/gmplot) with our train_set.
  We takes 5 random ids from the train_set and plot them onto a map creating 5 .html files that can be found into the  
  A_1htmls directory.  
  
 ### -A2_1: `dtwNeighbors.py`
 
  Using the dtw algorithm (https://pypi.org/project/fastdtw/ , not implemented by us) we find the top-5 trajectories that have  
  the smallest distance from each route in the a_1 test set. In A2_1htmls directory you will find plotted for each test_set element  
  the test itslef (named `original.#`) and the 5 closest tripIds. You will also find the result.txt which was the output that you will  
  receive as the module is being executed. It has info like computation time, distances and which bus lines where the closest ones.
  
 ### -A2_2: `lcssAlgorithm.py`

 From wikipedia (https://en.wikipedia.org/wiki/Longest_common_subsequence_problem):
 > The longest common subsequence (LCS) problem is the problem of finding the longest subsequence common to all sequences in a set of sequences (often just two sequences). It differs from the longest common substring problem: unlike substrings, subsequences are not required to occupy consecutive positions within the original sequences. The longest common subsequence problem is a classic computer science problem, the basis of data comparison programs such as the diff utility, and has applications in bioinformatics. It is also widely used by revision control systems such as Git for reconciling multiple changes made to a revision-controlled collection of files.  
   
 I suggest reading about the the way this algorithm works. As you can imagine it is really unlike for two points in two different trajectories to be exactly matching and having a haversine distance of 0km.  
For this reason we have a threshold of 0.2km. So if two points have a haversine distance smaller than 200 meters they are considered as common.  
On the final plots that you will find into A2_2htmls directory, you will see with green the train_set route and with red the LCS.   
On the results.txt you will also find which patternIds had the most common points and how many these points were.

 ### -A3: `knnClassification.py`
 
 We first find the top5 nearest neigbors according to the haversine distance. Then we perform the majority voting (without any weight) and the "elected" neighbor is written in the `A3_results/testSet_JourneyPatternIDs.csv` . 
 After that the module will also proceed on performing corss-validation with around 9% of the train_set which will take around 2 hours. Using a bigger percentage would result in more accurate results but the execution time would also increase more than we need to in our case.
 
