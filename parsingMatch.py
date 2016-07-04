from time import time
import sys as s

from misc import sanitize

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
        print lsClean[0]
        allSequences += lsClean[1:]
    return (filename,allSequences)

#Returns the list @allMatches such as @allMatches[i] is a pair (identifier of patient,list of identifiers of sequences matching a read in this patient) 
def parseAllMatch(filenames):
    allMatches = []
    start = time()
    try:
        for filename in filenames:
            if filename:
                allMatches.append(parseMatch(filename))
    except IOError:
        print "\nERROR: Maybe one of these filenames",filenames,"does not exist in \"meta/matches\" folder\n"
        s.exit(0)
    end = time()
    print "TIME .match:",(end-start)
    return allMatches
