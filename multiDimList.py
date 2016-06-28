#Not programming it as a class to use methods for lists

#@shape is a list of dimensions (integers)
#Returns a multi-dimensionnal list initialized with @init's
def initMDL(init,shape):
    mdList = init
    shape = shape[::-1]
    for dim in shape:
        if mdList == init:
            mdList = [ init for _ in range(dim) ]
        else:
            dimLists = []
            #To avoid an expensive deepcopy
            for i in range(dim):
                dimList = []
                for element in mdList:
                    dimList.append(element)
                dimLists.append(dimList)
            mdList = [ dimLists[i] for i in range(dim)]
    return mdList


def accessMDL(dimList,shape,mdl):
    if len(dimList) > len(shape):
        print "\n/!\ ERROR: Cannot access this multi-dimensionnal list."
        raise ValueError
    for i in dimList:
        n = len(mdl)
        if i > n or 0 > i:
            print "\n/!\ Dimension error."
            raise ValueError
        mdl = mdl[i]
    return mdl


def modifyMDL(dimList,newValue,shape,mdl):
    if len(dimList) > len(shape):
        print "\n/!\ ERROR: Cannot access this multi-dimensionnal list."
        raise ValueError
    lsList = [mdl]
    for i in dimList:
        n = len(lsList[-1])
        if i > n or 0 > i:
            print "\n/!\ Dimension error."
            raise ValueError
        newLs = []
        if isinstance(lsList[-1][i],list):
            for x in lsList[-1][i]:
                newLs.append(x)
            lsList.append(newLs)
    if not (len(dimList) == len(lsList) - 1):
        print "\n/!\ ERROR: Length error in [modifyMDL]:",len(dimList),(len(lsList)-1)
        raise ValueError
    dimList = dimList[::-1]
    while lsList and dimList:
        ls = lsList.pop()
        ls[dimList[-1]] = newValue
        newValue = []
        for x in ls:
            newValue.append(x)
        _ = dimList.pop()
    return ls

def test():
    ls = initMDL([],[2,3])
    print ls
    t = accessMDL([0,0],[2,3],ls)
    value = t.append(4)
    ls = modifyMDL([0,0],value,[2,3],ls)
    return ls
