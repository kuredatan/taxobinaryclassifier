from __future__ import division
#for training part in classification
from misc import partitionSampleByMetadatumValue
from randomSampling import randomChoice
import numpy as np

#@dataArray = [samplesInfoList,infoList,sampleIDList,idSequences,matchingNodes]

#Computes classes according to metadatum values
def computeClasses(dataArray,metadatum):
    #Any value in @valueSet is an integer (see partitionSampleByMetadatumValue)
    #@classes is a list containing partition of the samples ID according to the value of the metadatum
    valueSet,classes = partitionSampleByMetadatumValue(metadatum,dataArray[1],dataArray[0])
    if not valueSet:
        print "\n/!\ ERROR: metadatum",metadatum,"having abnormal values."
        raise ValueError
    return classes,valueSet

#______________________________________________________________________________________________________

#Training step #1: selects a random subset of the set of features vectors (samples)
#knuth=True uses Knuth's algorithm S, knuth=False uses Algorithm R
def selectTrainingSample(dataArray,n,knuth=False):
    #@dataArray[0] = sampleInfoList
    trainSubset,unchosen = randomChoice([sample[0] for sample in dataArray[0]],n,knuth)
    return trainSubset,unchosen

#______________________________________________________________________________________________________

#Training step #2: according to the values of metadatum, assigns a class to each sample of this subset
#@classes (see @computeClasses) is the known partition of the whole set of samples ID, that will be useful to
#compute the Youden's J coefficient
#returns @assignedClasses that is the partial partition of the set of samples restricted to the samples in @trainSubset
def assignClass(trainSubset,classes):
    assignedClasses = [ None for _ in classes ]
    for sampleID in trainSubset:
        numberClass = 0
        for class1 in classes:
            i = 0
            classLength = len(class1)
            while i < classLength and not (sampleID == class1[i][0]):
                i += 1
            if (i == classLength):
                #Search in next class
                numberClass += 1
            else:
                break
        #It means the sample has not been classed, meaning the value of metadatum for this sample is unknown
        if (i == classLength):
            continue
        else:
            if assignedClasses[numberClass]:
                assignedClasses[numberClass].append(sampleID)
            else:
                assignedClasses[numberClass] = [sampleID]
    return assignedClasses

#______________________________________________________________________________________________________

#Training step #3: computes the prior probability (also called posterior probability)
#of a certain node n of being in the whole training subset using Bayesian average (to deal with zero probabilities)

#Computes mean for a list of integer values
def computeMean(vList):
    n = len(vList)
    s = 0
    for v in vList:
        s += v
    return 1/n*s

#Returns an array @probList such as @probList[i] is the probability of having node @nodesList[i]
#For more details about the formula below, see the report at section about Bayesian average
def getPriorProbability(nodesList,trainSubset,dataArray):
    probList = []
    numberSstart = len(trainSubset)
    numberNodes = len(nodesList)
    #matchingNodes = @dataArray[4] is a dictionary of (key=name of sample,values=nodes matching in sample) pairs
    n = len(dataArray[4])
    #@nodesPresence is a list such as @nodesPresence[i][j] = 1 if node nodesList[i] matches in sample matchingNodes[j][0]
    #@dataArray[4] = @matchingNodes
    nodesPresence = [[0]*n]*numberNodes
    #@nodesPositive is a list such as @nodesPositive[i] is the number of samples in the training subset containing node @nodesList[i]
    nodesPositive = [0]*numberNodes
    for sample in trainSubset:
        j = 0
        while j < len(dataArray[0]) and not (sample == dataArray[0][j][0]):
            j += 1
        if (j == len(dataArray[0])):
            print "\n/!\ ERROR: Sample",sample,"not found."
            raise ValueError
        nodesSampleList = dataArray[4].get(sample)
        if nodesSampleList:
            i = 0
            for node in nodesList:
                nodesPresence[i][j] = int((node in nodesSampleList))
                #if @nodesPresence[i][j] == 1
                if nodesPresence[i][j]:
                    nodesPositive[i] += 1
                i += 1
    for i in range(numberNodes):
        M = nodesPositive[i]/numberSstart
        v = 0
        for j in range(numberSstart):
            v += (nodesPresence[i][j]-M)*(nodesPresence[i][j]-M)
        v = np.sqrt(v)
        c = numberSstart/(2*(v+1))
        m = c/numberSstart
        probList.append((c*m+nodesPositive[i])/(c+numberSstart))
    return probList,nodesPresence

#Returns @classes, which is the partition of the whole set of samples according to the values of metadatum
#and @assignedClasses the partial partition of the training subset of samples
#and @valuesClasses is the list of lists of (expectation,standard deviation) pairs for each node considered
#and @unchosen is the set of remaining samples to cluster
def trainingPart(dataArray,metadatum,nodesList,numberStartingSamples):
    n = len(nodesList)
    classes,valueSet = computeClasses(dataArray,metadatum)
    trainSubset,unchosen = selectTrainingSample(dataArray,numberStartingSamples)
    probList,nodesPresence = getPriorProbability(nodesList,trainSubset,dataArray)
    assignedClasses = assignClass(trainSubset,classes)
    return classes,valueSet,assignedClasses,unchosen,probList,nodesPresence
    
