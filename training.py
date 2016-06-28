#for training part in classification
from normalization import expectSTDevList
from misc import partitionSampleByMetadatumValue
from randomSampling import randomChoice
import numpy as np

#dataArray = [samplesInfoList,infoList,paths,n,nodesList,taxoTree,sampleIDList,featuresVectorList,matchingSequences]

#Computes classes according to metadatum values
def computeClasses(dataArray,metadatum):
    #Any value in @valueSet is an integer (see partitionSampleByMetadatumValue)
    #@classes is a list containing partition of the samples according to the value of the metadatum
    valueSet,classes = partitionSampleByMetadatumValue([metadatum],dataArray[1],dataArray[0])
    if not valueSet:
        print "\n/!\ ERROR: metadatum",metadatum,"having abnormal values."
        raise ValueError
    return classes

 #Training step #1: selects a random subset of the set of features vectors (samples)
 #knuth=True uses Knuth's algorithm S, knuth=False uses Algorithm R
def selectTrainingSample(dataArray,n,knuth=False):
    trainSubset = randomChoice(dataArray[7],n,knuth)
    return trainSubset

#@featureVector is a pair (sample name, list of (metadatum,value) pairs)
def giveValueMetadatum(featureVector,metadatum):
    #if @featureVector is not a pair
    if not (len(featureVector) == 2):
        print "\n/!\ ERROR: Feature vector error: length",len(featureVector)
        raise ValueError
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

def getNumberValueSet(valueSet,value):
    n = len(valueSet)
    while i < n and not (valueSet[i] == value):
        i += 1
    if i == n:
        print "\n/!\ ERROR: This value",value,"does not belong to the list:",valueSet,"."
        raise ValueError
    else:
        return i

#Training step #2: according to the values metadatum, assigns a class to each sample of this subset
#@classes (see @computeClasses) is the known partition of the whole set of samples, that will be useful to
#compute the Youden's J coefficient
#@assignedClasses is the partial partition of the set of samples restricted to the samples in @trainSubset
#MISSING LINK BETWEEN SAMPLES IN MATCHING SEQUENCES AND FEATURE VECTOR
def assignClass(trainSubset,classes):
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
    
