from __future__ import division
from misc import truncate

#Compute the TP,TN,FN,FP rates (see README)
#@n is the number of samples
#Returns the sum of J(C) for all classes C (see README)
def countYouden(classes,assignedClasses,n):
    youdenCoeffList = []
    classesCopy = []
    for class1 in classes:
        classesCopy.append(class1)
    assignedClassesCopy = []
    for class1 in assignedClasses:
        assignedClassesCopy.append(class1)
    while assignedClassesCopy and classesCopy:
        #for all i, @assignedClassesCopy[i] correspond to the same value of metadatum than @classes[i]
        class1,asClass1 = classesCopy.pop(),assignedClassesCopy.pop()
        tp,fp,fn = 0,0,0
        #TN = @n - FP - TP - FN
        for sample in class1:
            if (sample in asClass1):
                tp += 1
            else:
                fn += 1
        for sample in asClass1:
            if not (sample in class1):
                fp += 1
        tn = n - tp - fp - fn
        j = tp/(tp + fn) + tn/(tn + fp) - 1
        if j < -1 or j > 1:
            print "\n/!\ ERROR: Inconsistent value of Youden's J coefficient:",j,"."
            raise ValueError
        youdenCoeffList.append(j)
    s = 0
    for j in youdenCoeffList:
        s += j
    return s
    

def interpretIt(youdenJ):
    print youdenJ
