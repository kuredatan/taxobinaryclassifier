from random import randint

#Each element of elementList is associated to a unique patient/bacteria
#n is the size of the chosen set
#Implementation of Algorithm R (Algorithm S with knuth=True)
#Can be improved by returning also the set of unchosen elements
def randomChoice(elementList,n,knuth=False):
    m = len(elementList)
    if m == n:
        return elementList
    elif m < n:
        print "\n/!\ ERROR: Required set is bigger than set of available elements."
        raise ValueError
    reservoir = []
    for i in range(n):
        reservoir.append(elementList[i])
    for i in range(n,m):
        j = randint(1,i)
        if j <= n:
            if knuth:
                k = randint(1,n)
                reservoir[k] = elementList[i]
            else:
                reservoir[j] = elementList[i]
        return reservoir
