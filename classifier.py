from __future__ import division

from misc import mem

#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes]

#Computes Bayes's theorem
#Uses an hypothesis of Bernouilli naive distribution (that is, we are assuming the independance between the values of metadata) + equiprobability of being in one of the classes (that is, we are assuming that a sample can be equiprobably take one of the values of the total set of values of the metadatum), which are quite strong hypotheses (for a clearer explanation, see README)
#Returns a list @postMeasures containing class probabilities for each class such as @postMeasures[i] is the class probability for class @assignedClasses[i] (corresponding to pair valuesClasses[i])
#@numberClass = len(@valuesClasses) = len(@classes) = len(@assignedClasses)
def probabilityKnowingClass(nodesList,assignedClasses,dataArray,numberClass,probList,nodesPresence):
    #@probKnowingClass[i][j] is the probability of node nodesList[i] being in class assignedClass[j]
    probKnowingClass = []
    cl = 0
    nod = 0
    for node in nodesList:
        for class1 in assignedClasses:
            numberNodeAppearsInClass = 0
            for sample in class1:
                if nodesPresence[][]
            
    for node in nodesList:
        

def bayesCalculus(sample,nodesList,dataArray,numberClass,probList,nodesPresence):
    postMeasures = []
    #Equiprobability (could also be computed using the training subset, but we should have dealt with the zero probabilities)
    #with the bayesian average used for probabilities of having a node, but it would be as irrelevant, because interaction between
    #metadata values are depending on the real definition of the metadata (see data matrix)
    if not numberClass:
        print "\n/!\ ERROR: No class assigned."
        raise ValueError
    probBeingInClass = 1/numberClass
    #for each class
    for i in range(numberClass):
            
        
    normCt = probBeingInClass* + probBeingInClass*
    return postMeasures

#Returns @assignedClasses (partition of the whole set of samples according to node population)
#and @classes (partition of the whole set of samples according to the values of metadatum)
def classifyIt(dataArray,metadatum,nodesList):
    #@assignedClasses is the current partial partition of the set of samples
    #@classes is the partition of the whole set of samples (to compute Youden's J coefficient)
    #@unchosen is the set of samples remaining to be clustered
    #@probList is a list such as @probList[i] is the prior probability of having node @nodesList[i] in a sample
    classes,assignedClasses,unchosen,probList,nodesPresence = trainingPart(dataArray,metadatum,nodesList)
    numberClass = len(classes)
    if not (len(numberClass == len(assignedClasses)):
        print "\n/!\ ERROR: Length error: classes:",numberClass,"assignedClasses",len(assignedClasses),"."
        raise ValueError
    for sample in unchosen:
        postMeasures = bayesCalculus(sample,nodesList,dataArray,numberClass,probList,nodesPresence)
        #Gets the highest class probability in @postMeasures
        maxIndex = 0
        maxProb = 0
        n = len(postMeasures)
        for i in range(n):
            if maxProb < postMeasures[i]:
                maxProb = postMeasures[i]
                maxIndex = i
        #Assigning this sample to the class number @maxIndex
        assignedClasses[maxIndex] = assignedClasses[maxIndex].append(sample)
    return assignedClasses
