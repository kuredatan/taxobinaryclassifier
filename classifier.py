#Computes Bayes's theorem
#Returns a list @postMeasures containing class probabilities for each class, and the array @hashInt such as @postMeasures[i] is the class probability of class @hashInt[i] (@hashInt[i] is the list such as accessMDL[@hashInt[i]] is the class associated)
def bayesCalculus(sample,valuesClasses,nodesList,dataArray):
    ()

#Returns @assignedClasses (partition of the whole set of samples according to node population)
#and @classes (partition of the whole set of samples according to the values of metadatum)
def classifyIt(dataArray,metadatum,nodesList):
    #@valuesClasses is a list containing lists of (node,expectation,standard deviation) pairs (for each class)
    #@assignedClasses is the current partial partition of the set of samples
    #@classes is the partition of the whole set of samples (to compute Youden's J coefficient)
    #@unchosen is the set of samples remaining to be clustered
    classes,assignedClasses,valuesClasses,unchosen = trainingPart(dataArray,metadatum,nodesList)
    for sample in unchosen:
        postMeasures,hashInt = bayesCalculus(sample,valuesClasses,nodesList,dataArray)
        maxIndex = 0
        maxProb = 0
        n = len(postMeasures)
        dim = 1
        for x in shape:
            dim = dim*x
        if not (n == dim):
            print "\n/!\ ERROR: Length error",n,dim,"."
            raise ValueError
        for i in range(n):
            if maxProb < postMeasures[i]:
                maxProb = postMeasures[i]
                maxIndex = i
        #Assigning this feature vector to the class number i
        dimList = hashInt[i]
        previousClass = accessMDL(dimList,shape,assignedClasses)
        newValue = previousClass.append(featureVector)
        assignedClasses = modifyMDL(dimList,newValue,shape,assignedClasses)
    return assignedClasses
