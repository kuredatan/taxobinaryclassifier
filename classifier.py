from __future__ import division

from misc import mem

#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes]

#Computes Bayes's theorem
#Uses an hypothesis of Bernouilli naive distribution (that is, we are assuming the independance between the values of metadata) + equiprobability of being in one of the classes (that is, we are assuming that a sample can be equiprobably take one of the values of the total set of values of the metadatum), which are quite strong hypotheses (for a clearer explanation, see README)
#Returns a list @postMeasures containing class probabilities for each class such as @postMeasures[i] is the class probability for class @assignedClasses[i] (corresponding to pair valuesClasses[i])
#@numberClass = len(@valuesClasses) = len(@classes) = len(@assignedClasses)
def bayesCalculus(sample,nodesList,dataArray,numberClass,numberNode):
    postMeasures = []
    nodesPresence = [0]*numberNode
    #Equiprobability (could also be computed using the training subset, but we should have dealt with the zero probabilities)
    probBeingInClass = 1/numberClass
    probHavingNode = 1/2
    i = 0
    #@dataArray[5] = matchingNodes
    n = len(dataArray[5])
    while i < n and not (matchingNodes[i][0] == sample):
        if not (len(matchingNodes[i]) == 2):
            print "\n/!\ ERROR: Incorrect match length",len(matchingNodes),"."
            raise ValueError
        i += 1
    if (i == n):
        print "\n/!\ ERROR: This sample",sample,"is not in matchingNodes."
        raise ValueError
    else:
        nodList = matchingNodes[i][1]
        for node in nodList:
            nodesPresence[i] = int(mem(nod,nodesList))
            
        
    normCt = probBeingInClass* + probBeingInClass*
    return postMeasures

#Returns @assignedClasses (partition of the whole set of samples according to node population)
#and @classes (partition of the whole set of samples according to the values of metadatum)
def classifyIt(dataArray,metadatum,nodesList):
    #@assignedClasses is the current partial partition of the set of samples
    #@classes is the partition of the whole set of samples (to compute Youden's J coefficient)
    #@unchosen is the set of samples remaining to be clustered
    classes,assignedClasses,unchosen = trainingPart(dataArray,metadatum,nodesList)
    numberNode = len(dataArray[2])
    numberClass = len(classes)
    if not (len(numberClass == len(assignedClasses)):
        print "\n/!\ ERROR: Length error: classes:",numberClass,"assignedClasses",len(assignedClasses),"."
        raise ValueError
    for sample in unchosen:
        postMeasures = bayesCalculus(sample,nodesList,dataArray,numberClass,numberNode)
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
