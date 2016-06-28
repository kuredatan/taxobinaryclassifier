from multiDimList import accessMDL,initMDL,modifyMDL

#Computes Bayes's theorem
#Returns a list @postMeasures containing class probabilities for each class, and the array @hashInt such as @postMeasures[i] is the class probability of class @hashInt[i] (@hashInt[i] is the list such as accessMDL[@hashInt[i]] is the class associated)
def bayesCalculus(featureVector,assignedClasses,valuesClasses,shape,nodesList,dataArray):
    ()

#Returns a (multi-dimensionnal list) MDL containing the list of features vector in this class
def classifyIt(dataArray,metadataList,nodesList):
    #@values classes is a list containing lists of (node,expectation,standard deviation) pairs (for each class)
    #@assignedClasses is the current MDL of the classes
    #@shape is a list containing the dimensions of @assignedClasses
    valuesClasses,assignedClasses,shape = trainingPart(dataArray,metadataList,nodesList)
    #@dataArray[7] = featuresVectorList
    for featureVector in dataArray[7]:
        postMeasures,hashInt = bayesCalculus(featureVector,assignedClasses,valuesClasses,shape,nodesList,dataArray)
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
