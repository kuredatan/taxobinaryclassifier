from __future__ import division
#for training part in classification
from misc import partitionSampleByMetadatumValue,mem
from randomSampling import randomChoice
import numpy as np

#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes]

#Computes classes according to metadatum values
def computeClasses(dataArray,metadatum):
    #Any value in @valueSet is an integer (see partitionSampleByMetadatumValue)
    #@classes is a list containing partition of the samples ID according to the value of the metadatum
    valueSet,classes = partitionSampleByMetadatumValue([metadatum],dataArray[1],dataArray[0])
    if not valueSet:
        print "\n/!\ ERROR: metadatum",metadatum,"having abnormal values."
        raise ValueError
    return classes,valueSet

#______________________________________________________________________________________________________

#Training step #1: selects a random subset of the set of features vectors (samples)
#knuth=True uses Knuth's algorithm S, knuth=False uses Algorithm R
def selectTrainingSample(dataArray,n,knuth=False):
    #@dataArray[3] = sampleIDList, that matches samples in featuresVectorList
    trainSubset,unchosen = randomChoice(dataArray[3],n,knuth)
    return trainSubset,unchosen

#______________________________________________________________________________________________________

#Training step #2: according to the values of metadatum, assigns a class to each sample of this subset
#@classes (see @computeClasses) is the known partition of the whole set of samples ID, that will be useful to
#compute the Youden's J coefficient
#returns @assignedClasses that is the partial partition of the set of samples restricted to the samples in @trainSubset
def assignClass(trainSubset,classes):
    classLength = [ len(class1) for class1 in classes ]
    assignedClasses = [ [] for _ in classes ]
    for sampleID in trainSubset:
        numberClass = 0
        for class1 in classes:
            i = 0
            while i < classLength[numberClass] and not (sampleID == classes[numberClass][i]):
                i += 1
            if (i == classLength[numberClass]):
                #Search in next class
                numberClass += 1
            else:
                break
        if (i == classLength[-1]):
                print "\n/!\ ERROR: Sample ID",sampleID,"is not in the classes",classes[0],"\nnor",classes[1],"."
                raise ValueError
        else:
            assignedClasses[numberClass] = assignedClasses[numberClass].append(sampleID)
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
def getPriorProbability(nodesList,trainSubset,dataArray):
    probList = []
    #The number of nodes being both in @nodesList and in the matching lists of samples in the training set
    numberNodesInTrainSubset = 0
    numberNodes = len(nodesList)
    numberSamples = len(trainSubset)
    #matchingNodes = @dataArray[5] is a list of (name of sample,nodes matching in sample) pairs
    n = len(dataArray[5])
    #@nodesPresence is a list such as @nodesPresence[i][j] = 1 if node nodesList[i] matches in sample matchingNodes[j][0]
    #@dataArray[8] = @matchingNodes
    nodesPresence = [[0]*len(dataArray[5])]*numberNodes
    #@nodesPositive is a list such as @nodesPositive[i] is the number of samples in the training subset containing node @nodesList[i]
    nodesPositive = [0]*numberNodes
    for sample in trainSubset:
        j = 0
        while j < n and not (sample == dataArray[5][j][0]):
            if not (len(dataArray[5][j]) == 2):
                print "\n/!\ ERROR: Pair length error:",len(pair),"."
                raise ValueError
            j += 1
        if (j == n):
            print "\n/!\ ERROR: Sample",sample,"not in matchingNodes."
            raise ValueError
        else:
            nodesSampleList = dataArray[5][j][1]
            i = 0
            for node in nodesList:
                nodesPresence[i][j] = int(mem(node,nodesSampleList))
                #if @nodesPresence[i][j] == 1
                if nodesPresence[i][j]:
                    nodesPositive[i] += 1
                    numberNodesInTrainSubset += 1
                i += 1
    for i in range(numberNodes):
        m = computeMean(nodesPresence[i])
        probList.append((nodesPositive[i]*m + numberNodesInTrainSubset)/(nodesPositive[i] + numberSamples))
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
    assignedClasses = assignClass(dataArray,trainSubset,classes)
    return classes,valueSet,assignedClasses,unchosen,probList,nodesPresence
    
