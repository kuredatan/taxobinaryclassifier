from __future__ import division
#for training part in classification
from misc import partitionSampleByMetadatumValue,mem
from randomSampling import randomChoice
import numpy as np

#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes]

#MISSING LINK BETWEEN SAMPLES IN @MATCHINGNODES AND @FEATURESVECTORLIST
def convertFeaturesIntoMatching(featuresVectorList,matchingNodes,sampleID):
    return sampleID

def convertMatchingIntoFeatures(featuresVectorList,matchingNodes,sampleID):
    return sampleID

#Computes classes according to metadatum values
def computeClasses(dataArray,metadatum):
    #Any value in @valueSet is an integer (see partitionSampleByMetadatumValue)
    #@classes is a list containing partition of the samples ID according to the value of the metadatum
    valueSet,classes = partitionSampleByMetadatumValue([metadatum],dataArray[1],dataArray[0])
    if not valueSet:
        print "\n/!\ ERROR: metadatum",metadatum,"having abnormal values."
        raise ValueError
    return classes

#______________________________________________________________________________________________________

#Training step #1: selects a random subset of the set of features vectors (samples)
#knuth=True uses Knuth's algorithm S, knuth=False uses Algorithm R
def selectTrainingSample(dataArray,n,knuth=False):
    #@dataArray[3] = sampleIDList, that matches samples in featuresVectorList
    trainSubset = randomChoice(dataArray[3],n,knuth)
    return trainSubset,unchosen

#______________________________________________________________________________________________________

#@featureVector is a pair (sample name, list of (metadatum,value) pairs)
def giveValueMetadatum(featureVector,metadatum):
    #if @featureVector is not a pair
    if not (len(featureVector) == 2):
        print "\n/!\ ERROR: Feature vector error: length",len(featureVector),"."
        raise ValueError
    #list of (metadatum,value) pairs
    ls = featureVector[1]
    for pair in ls:
        if not (len(pair) == 2):
            print "\n/!\ ERROR: Pair dimension error: length",len(pair),"."
            raise ValueError
        elif (pair[0] == metadatum):
            return pair[1]
    #If there is no pair corresponding to the metadatum in the list
    print "\n/!\ ERROR: This metadatum",metadatum,"does not exist in the feature vector of sample",featureVector[0],"."
    raise ValueError

#To get the number of the class associated
def getNumberValueSet(valueSet,value):
    n = len(valueSet)
    while i < n and not (valueSet[i] == value):
        i += 1
    if i == n:
        print "\n/!\ ERROR: This value",value,"does not belong to the list:",valueSet,"."
        raise ValueError
    else:
        return i

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
    #matchingNodes = @dataArray[8] is a list of (name of sample,nodes matching in sample) pairs
    n = len(dataArray[8])
    #@nodesPresence is a list such as @nodesPresence[i][j] = 1 if node nodesList[i] matches in sample trainSubset[j]
    nodesPresence = [[0]*numberSamples]*numberNodes
    #@nodesPositive is a list such as @nodesPositive[i] is the number of samples in the training subset containing node @nodesList[i]
    nodesPositive = [0]*numberNodes
    for sample in trainSubset:
        j = 0
        while i < n and not (convertFeaturesIntoMatching(dataArray[7],dataArray[8],sample) == dataArray[8][j][0]):
            if not (len(dataArray[8][j]) == 2):
                print "\n/!\ ERROR: Pair length error:",len(pair),"."
                raise ValueError
            j += 1
        if (j == n):
            print "\n/!\ ERROR: Sample",sample,"not in matchingNodes."
            raise ValueError
        else:
            nodesSampleList = dataArray[8][j][1]
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

#Training step #3: computes expectation and standard deviation for the different criteria over nodes for each class
#@nodesList is the list of (name,rank) of considered nodes
#@matchingNodes contains (sampleID,list of nodes (name,rank) matching a read in this sample) pairs
#def getListFromMatchingNodes(matchingNodes,sampleID):
#    i = 0
#    n = len(matchingNodes)
#    while i < n and not (matchingNodes[i][0] == sampleID):
#        if not (len(matchingNodes[i]) == 2):
#            print "\n/!\ ERROR: matchingNodes formatting incorrect: length:",len(matchingNodes[i]),"."
#            raise ValueError
#        i += 1
#    if (i == n):
#        print "\n/!\ ERROR: Sample",sampleID,"not in matchingNodes."
#        raise ValueError
#    else:
#        return matchingNodes[i]

def getPlaceInNodesList(node,nodesList,n):
    i = 0
    while i < n and not (node == nodesList[i]):
        i += 1
    if (i == n):
        print "\n/!\ ERROR: Node",node,"is not in nodesList",nodesList,"."
        raise ValueError
    else:
        return i

#@n = len(@nodesList)
#@m = len(@class1)
#def computeExpectSTDev(dataArray,class1,nodesList,n,m):
#    #@valuesClass contains (node,expectation,standard deviation) tuples
#    valuesClass = []
#    #@nodesPresence[i][j] = 1 if @nodesList[i] matches a read in @class1[j], otherwise 0
#    nodesPresence = np.zeros((n,m))
#    for i in range(m):
#        sampleIDNode = convertFeaturesIntoMatching(dataArray[7],dataArray[8],class1[i])
#        nodesListMatch = getListFromMatchingNodes(dataArray[8],sampleIDNode)
#        for node in nodesList:
#            if not (len(node) == 2):
#                print "\n/!\ ERROR: node error: length",len(node),"."
#                raise ValueError
#            elif mem(node,nodesListMatch):
#                index = getPlaceInNodesList(node,nodesList,n)
#                #see @getPlaceInNodesList: i < n 
#                nodesPresence[index][i] = 1
#    for i in range(n):
#        expectation,stdev = expectSTDevList(nodesPresence[i])
#        valuesClass.append((nodesList[i],expectation,stdev))
#    return valuesClass

#Returns @classes, which is the partition of the whole set of samples according to the values of metadatum
#and @assignedClasses the partial partition of the training subset of samples
#and @valuesClasses is the list of lists of (expectation,standard deviation) pairs for each node considered
#and @unchosen is the set of remaining samples to cluster
def trainingPart(dataArray,metadatum,nodesList):
    n = len(nodesList)
    classes = computeClasses(dataArray,metadatum)
    #len(classes): enough? 
    trainSubset,unchosen = selectTrainingSample(dataArray,len(classes))
    probList,nodesPresence = getPriorProbability(nodesList,trainSubset,dataArray)
    assignedClasses = assignClass(dataArray,trainSubset,classes)
    #len(@assignedClasses) == 2 (see @assignClass)
    #m1 = len(assignedClasses[0])
    #m2 = len(assignedClasses[1])
    #valuesClass1 = computeExpectSTDev(dataArray,assignedClasses[0],nodesList,n,m1)
    #valuesClass2 = computeExpectSTDev(dataArray,assignedClasses[1],nodesList,n,m2)
    return classes,assignedClasses,unchosen,probList,nodesPresence #[valuesClass1,valuesClass2]
    
