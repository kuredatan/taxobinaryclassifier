from parsingTree import parseTree
from parsingInfo import parseInfo
from taxoTree import TaxoTree
from actions import userNodeSelectionAct,randomSubSamplingAct,printTreeAct,parseList
from featuresVector import featuresCreate
from misc import getSampleIDList

def main():
    tTree = raw_input("Write down the file name of the taxonomic tree in the folder \"meta\" [ without the extension .tree ]\n")
    if (tTree == ""):
        tTree = "GGdb2015"
    iMatrix = raw_input("Write down the CSV file name of the data matrix in the folder \"meta\" [ without the extension .csv ]\n")
    if (iMatrix == ""):
        iMatrix = "Info"
    iMatrix = raw_input("Write down the CSV file name of the data matrix in the folder \"meta\" [ without the extension .csv ]\n")
    if (iMatrix == ""):
        iMatrix = "Info"
    filenames = parseList(raw_input("Write down the MATCH file names in the folder \"meta/match\" [ without the extension .match ] [e.g. BC_M0;GC_M0 ] \n"))
    if (filenames == ""):
        filenames = ["BC_M0_good","DC_M0_good","GC_M0_good","TR_M0_good","BC_M3_good","DC_M3_good","GC_M3_good","TR_M3_good","BJ_M0_good","EY_M0_good","GM_M0_good","BJ_M3_good","EY_M3_good","GM_M3_good"]
    fastaFileName = raw_input("Write down the MATCH file names in the folder \"meta/match\" [ without the extension .match ]\n")
    if (fastaFileName == ""):
        fastaFileName = "GREENGENES_gg16S_unaligned_10022015"
    print "/!\ Data getting parsed..."
    try:
        samplesInfoList,infoList = parseInfo(iMatrix)
        sampleIDList = getSampleIDList(samplesInfoList)
    except IOError:
        print "\nERROR: Maybe the filename you gave does not exist in \"meta\" folder\n"
    print "..."
    try:
        samplesOccList,speciesList = parseMatrix(oMatrix)
    except IOError:
        print "\nERROR: Maybe the filename you gave does not exist in \"meta\" folder\n"
    print "..."
    try:
        paths,n,nodesList = parseTree(tTree)
    except IOError:
        print "\nERROR: Maybe the filename you gave does not exist in \"meta\" folder\n"
    print "-- End of parsing\n"
    print "/!\ Constructing the whole annotated taxonomic tree"
    print "[ You may have to wait for a few seconds... ]"
    taxoTree = TaxoTree("Root").addNode(paths,nodesList,samplesOccList)
    print "-- End of construction\n"
    print "/!\ Constructing the features vectors..."
    featuresVectorList,matchingSequences,idSequences,phyloSequences = featuresCreate(sampleInfoList,infoList,filenames,fastaFileName)
    print "-- End of construction\n"
    dataArray = [samplesInfoList,infoList,paths,n,nodesList,taxoTree,sampleIDList,featuresVectorList,matchingSequences,idSequences,phyloSequences]
    answer = ""
    while not ((answer == "exit") or (answer == "exit()") or (answer == "quit")):
        try:
            print "What do you want to do?"
            print "[Write down the number matching with the action required. Details are in README file]"
            print "   1: User node selection"
            print "   2: Random sub-sampling"
            print "   3: Print the taxonomic tree"
            print "[To quit, write down exit]"
            answer = raw_input("Your answer?\n")
            if (answer =="1"):
                userNodeSelectionAct(dataArray)
                print "-- End \n"
            elif (answer == "2"):
                randomSubSamplingAct(dataArray)
                print "-- End \n"
            elif (answer == "3"):
                printTreeAct(dataArray)
                print "-- End \n"
            elif not ((answer == "exit") or (answer == "exit()") or (answer == "quit")):
                print "/!\ ERROR: Please enter a number between 1 and 3 included, or 'exit' if you want to quit."
                raise ValueError
        except ValueError:
            print "/!\ ERROR: Please look at the line above."
C            print "/!\ ERROR: If the line above is blank, it may be an uncatched ValueError.\n"
    #return dataArray    