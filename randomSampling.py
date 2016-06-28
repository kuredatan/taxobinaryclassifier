from random import randint

#Each element of elementList is associated to a unique patient/bacteria
#n is the size of the chosen set
#Implementation of Algorithm R (Algorithm S with knuth=True)
#returns the reservoir and the set of unchosen elements such as {reservoir,unchosen} is a partition of the initial set of elements

#When element is selected to be @reservoir[k], deletes it (if exists) from @unchosen
#@m is the length of the total list, and also the length of @unchosen
def swap(element,reservoir,k,unchosen,m):
    j = 0
    while j < m and not (unchosen[j] == element):
        j += 1
    #Means @element is already in @reservoir
    if (j == m):
        reservoir[k] = element
    else:
        unchosen[j] = reservoir[k]
        reservoir[k] = element
    return reservoir,unchosen

def cleanNone(unchosen):
    return [x for x in unchosen if not (x == None)]

def randomChoice(elementList,n,knuth=False):
    m = len(elementList)
    if m == n:
        return elementList
    elif m < n:
        print "\n/!\ ERROR: Required set is bigger than set of available elements."
        raise ValueError
    reservoir = elementList[:n]
    unchosen = [None]*n + elementList[n:]
    for i in range(n,m):
        j = randint(0,i)
        if j < n:
            if knuth:
                k = randint(0,n-1)
                reservoir,unchosen = swap(elementList[i],reservoir,k,unchosen,m)
            else:
                reservoir,unchosen = swap(elementList[i],reservoir,j,unchosen,m)
    unchosen = cleanNone(unchosen)    
    return reservoir,unchosen
