from parsingMatch import parseAllMatch
from parsingFasta import parseFasta

#Creates for each patient the corresponding features vector and matching nodes, that is:
#@featuresVectorList is the list of @featuresVector such as @featuresVector is a pair
#(@name of sample/patient,list of (metadatum,value for this patient in the data matrix) pairs)
#and @matchingNodes is the list of pairs (name of patient,list of nodes matched in this sample that is a (name,rank) list)

#Default phylogeny is GreenGenes'
def getNextRank(rank,ranks=["R","K","P","C","O","F","G","S"]):
    i = 0
    n = len(ranks)
    while i < n and not (rank == ranks[i]):
        i += 1
    if (i == n):
        print "\n/!\ ERROR: Wrong phylogeny (1). Please change the ranks array in featuresVector.py."
        raise ValueError
    elif (i == n-1):
        print "\n/!\ ERROR: Wrong phylogeny (2). Please change the ranks array in featuresVector.py."
        raise ValueError
    else:
        return ranks[i+1]

def getCorrespondingID(sequenceID,idSequences):
    i = 0
    n = len(idSequences)
    while i < n and not idSequences[i] == sequenceID:
        i += 1
    if (i == n):
        print "\n/!\ ERROR: sequence not in idSequences."
        raise ValueError
    return i

def getNodeAssociated(sequenceID,idSequences,phyloSequences):
    index = getCorrespondingID(sequenceED,idSequences)
    if not (len(phyloSequences[index][-1]) == 2):
        print "\n/!\ ERROR: [BUG] [featuresVector/getNodeAssociated] Wrong node length:",len(phyloSequences[index][-1]),"."
        raise ValueError
    fatherRank = phyloSequences[index][-1][1]
    rank = getNextRank(fatherRank)
    if not (len(idSequences[index]) == 2):
        print "\n/!\ ERROR: [BUG] [featuresVector/getNodeAssociated] Wrong pair length:",len(idSequences[index]),"."
        raise ValueError
    name = idSequences[index][1]
    return (name,rank)

#@allMatches is a list of (sample ID,list of sequences ID matching a read in this sample) pairs (see parsingMatch.py)
#returns a list of (sample ID,list of nodes (name,rank) matching a read in this sample) pairs
def getMatchingNodes(allMatches,idSequences,phyloSequences):
    matchingNodes = []
    for pair in allMatches:
        if not len(pair) == 2:
            print "\n/!\ ERROR: Incorrect matches formatting."
            raise ValueError
        sampleID = pair[0]
        matchingSequences = pair[1]
        matchingThisSampleNodes = []
        for sequenceID in matchingSequences:
            matchingThisSampleNodes.append(getNodeAssociated(sequenceID,idSequences,phyloSequences))
        matchingNodes.append((sampleID,matchingThisSampleNodes))
    return matchingNodes
        
#Returns @featuresVectorList and @matchingNodes
#@filenames is the list of .match file names
#@fastaFileName is a string of the .fasta file name
def featuresCreate(sampleInfoList,infoList,filenames,fastaFileName):
    print "/!\ Parsing .match files"
    print "[ You may have to wait a few minutes... ]"
    try:
        allMatches = parseAllMatch(filenames)
    except IOError:
        print "\nERROR: Maybe the filename you gave does not exist in \"meta/matches\" folder\n"
    print "/!\ Parsing .fasta files"
    print "[ You may have to wait a few minutes... ]"
    try:
        idSequences,phyloSequences = parseFasta(fastaFileName)
    except IOError:
        print "\nERROR: Maybe the filename you gave does not exist in \"meta\" folder\n"    
    #Link between file name and sample name?
    #--------------CONSTRUCTING @featuresVectorList
    featuresVectorList = []
    for sample in sampleInfoList:
        print sample[0]
        n = len(sample)
        if n < 1:
            print "\n/!\ ERROR: Sample info incorrect."
            raise ValueError
        metadataList = []
        for i in range(1,n):
            metadataList.append((infoList[i],sample[i]))
        featuresVectorList.append((sample[0],metadataList))
    #--------------CONSTRUCTING @matchingNodes
    matchingNodes = getMatchingNodes(allMatches,idSequences,phyloSequences)
    return featuresVectorList,matchingNodes

def test():
    from parsingInfo import parseInfo
    sampleInfoList,infoList = parseInfo("Info")
    featuresVectorList,matchingNodes = featuresCreate(sampleInfoList,infoList,["BC_M0_good","DC_M0_good"],"test")
    return featuresVectorList[:3],matchingSequences[:3]
