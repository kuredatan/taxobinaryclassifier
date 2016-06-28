#for training part in classification
from normalization import expectSTDevList
from misc import partitionSampleByMetadatumValue
from multiDimList import initMDL,accessMDL,modifyMDL
from randomSampling import randomChoice
import numpy as np

#dataArray = [samplesInfoList,infoList,paths,n,nodesList,taxoTree,sampleIDList,featuresVectorList,matchingSequences]

#Computes classes according to metadata values
def computeClasses(dataArray,metadataList):
    valueSets = []
    shape = []
    metadataLength = 0
    for metadatum in metadataList:
        metadataLength += 1
        #Any value in @valueSet is an integer (see partitionSampleByMetadatumValue)
        valueSet,_ = partitionSampleByMetadatumValue([metadatum],dataArray[1],dataArray[0])
        if not valueSet:
            print "\n/!\ ERROR: metadatum",metadatum,"having abnormal values."
            raise ValueError
        valueSets.append(valueSet)
        shape.append(len(valueSet))
    if not (metadataLength == len(valueSets)):
        print "\n/!\ ERROR: Different lengths",len(valueSets),metadataLength
        raise ValueError
    classes = initMDL([],shape)
    return classes,shape,valueSets

 #Training step #1: selects a random subset of the set of features vectors (samples)
 #knuth=True uses Knuth's algorithm S, knuth=False uses Algorithm R
def selectTrainingSample(dataArray,n,knuth=False):
    trainSubset = randomChoice(dataArray[7],n,knuth)
    return trainSubset

#@featureVector is a pair (sample name, list of (metadatum,value) pairs)
def giveValueMetadatum(featureVector,metadatum):
    if not (len(featureVector) == 2):
        print "\n/!\ ERROR: Feature vector error: length",len(featureVector)
        raise ValueError
    ls = featureVector[1]
    for pair in ls:
        if not (len(pair) == 2):
            print "\n/!\ ERROR: Pair dimension error: length",len(pair)
            raise ValueError
        elif (pair[0] == metadatum):
            return pair[1]
    print "\n/!\ ERROR: This metadatum",metadatum,"does not exist in the feature vector of sample",featureVector[0],"."
    raise ValueError

def getNumberValueSet(valueSet,value):
    n = len(valueSet)
    while i < n and not (valueSet[i] == value):
        i += 1
    if i == n:
        print "\n/!\ ERROR: This value",value,"does not belong to the list:",valueSet
        raise ValueError
    else:
        return i

#Training step #2: according to metadata, assigns a class to each sample of this subset
def assignClass(dataArray,trainSubset,classes,shape,valueSets,metadataList):
    for featureVector in trainSubset:
        #dimensions to access to the class
        finalClass = []
        n = len(metadatum)
        for i in range(n):
            value = giveValueMetadatum(featureVector,metadataList[i]))
            dim = getNumberValueSet(valueSets[i],value)
            finalClass.append(dim)
        #Assign the whole feature vector to this class
        previousClass = accessMDL(finalClass,shape,classes)
        newValue = previousClass.append(featureVector)
        classes = modifyMDL(finalClass,newValue,shape,classes)
    return classes

#Link between @featuresVectors and @matchingSequences?
#@idSequences contains (sequence ID,reads matching) pairs
#@matchingSequences 
def getExpectSTdev(matchingSequences,idSequences):
    ()

#Training step #3: computes expectation and standard deviation for the different criteria over nodes for each class
def computeExpect(dataArray,assignedClasses,shape,nodesList):
    expectSTDevList
    
def trainingPart(dataArray,metadataList,nodesList):
    classes,shape,valueSets = computeClasses(dataArray,metadataList)
    #len(classes): enough? 
    trainSubset = selectTrainingSample(dataArray,len(classes))
    assignedClasses = assignClass(dataArray,trainSubset,classes,shape,valueSets,metadataList)
    valuesClasses = computeExpect(dataArray,assignedClasses,shape,nodesList)
    return valuesClasses,assignedClasses,shape
    
