#Centralization-reduction for a list of values
import numpy as np

from misc import inf

#Hypothesis of uniform probability for the occurrence of any bacteria whatever the clinic data may be (which is a strong hypothesis...)
def expectList(vList):
    n = len(vList)
    if not n:
        print "\n/!\ ERROR: Empty list."
        raise ValueError
    exp = 0
    for i in range(n):
        exp += vList[i]/n
    return exp

#Returns expectation and standard deviation
def expectSTDevList(vList):
    vProductList = [x*x for x in vList]
    expProd = expectList(vProductList)
    exp = expectList(vList)
    expS = exp*exp
    return exp,np.sqrt(expProd-expS)

def normalizeList(valueList):
    exp,stDev = expectSTDevList(valueList)
    if not stDev:
        print "\n/!\ ERROR: Math problem (Division by zero)."
        raise ValueError
    normList = []
    for value in valueList:
        normList.append((value-exp)/stDev)
    return normList
