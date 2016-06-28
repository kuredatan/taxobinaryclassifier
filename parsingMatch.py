from misc import sanitize
from time import time

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename):
    allSequences = []
    file_match = open("meta/match/" + filename + ".match","r")
    lines = file_match.readlines()
    file_match.close()
    #Each line corresponds to a read of this patient
    for read in lines:
        lsDirty = read.split(" ")
        lsClean = []
        #Last string is "\n"
        for string in lsDirty[:-1]:
            lsClean.append(sanitize(string))
        if len(lsClean) < 1:
            print "\n/!\ ERROR: MATCH parsing error:",len(lsClean),"."
            raise ValueError
        print "read",lsClean[0]
        allSequences += lsClean[1:]
    return (filename,allSequences)

#Returns the list @allMatches such as @allMatches[i] is a pair (identifier of patient,list of identifiers of sequences matching a read in this patient) 
def parseAllMatch(filenames):
    allMatches = []
    start = time()
    for filename in filenames:
        print "filename",filename
        allMatches.append(parseMatch(filename))
    end = time()
    print "TIME:",(end-start)
    return allMatches
    
