from __future__ import division
import numpy as np
import re
import random as rand

from writeOnFiles import writeFile
from misc import isInDatabase,getMaxMin,sanitize,inf
from classifier import classifyIt
from youden import countYouden,interpretIt
from randomSampling import randomChoice

from plottingValues import plotPie

#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes]

integer = re.compile("[0-9]+")

#Parsing functions
def parseList(string):
    if not (len(string.split(",")) == 1):
        print "\n/!\ ERROR: Do not use ',' as a separator: rather use ';'."
        raise ValueError
    elif not (len(string.split(":")) == 1):
        print "\n/!\ ERROR: Do not use ':' as a separator: rather use ';'."
        raise ValueError
    return string.split(";")

def parseListNode(string):
    if not (len(string.split(":")) == 1):
        print "\n/!\ ERROR: Do not use ':' as a separator: rather use ';'."
        raise ValueError
    ls = string.split(";")
    res = []
    for node in ls:
        nodeSplit = node.split(",")
        if not (len(nodeSplit) == 2):
            print "\n/!\ ERROR: Please use ',' as a separator for name,rank of a bacteria."
            raise ValueError
        nodeSplitName = nodeSplit[0].split("(")
        if not (len(nodeSplitName) == 2):
            print "\n/!\ ERROR: Please use the syntax '([name],[rank])' for each bacteria."
            raise ValueError
        nodeSplitRank = nodeSplit[-1].split(")")
        if not (len(nodeSplitRank) == 2):
            print "\n/!\ ERROR: Please use the syntax '([name],[rank])' for each bacteria."
            raise ValueError
        name,rank = nodeSplitName[-1],nodeSplitRank[0]
        res.append((name,rank))
    return res

def parseIntList(string):
    if not (len(string.split(",")) == 1):
        print "\n/!\ ERROR: Do not use ',' as a separator: rather use ';'."
        raise ValueError
    elif not (len(string.split(":")) == 1):
        print "\n/!\ ERROR: Do not use ':' as a separator: rather use ';'."
        raise ValueError
    l = string.split(";")
    resultList = []
    for s in l:
        if integer.match(s):
            resultList.append(int(s))
        elif s == "+inf" or s == "-inf":
            resultList.append(s)
        else:
            print "\n/!\ ERROR: Here you can only use integers or '+inf' or '-inf'."
            raise ValueError
    return resultList

#___________________________________________________________________________

#Macros for formatting
#Printing pretty lists of nodes
def listNodes(nodeList):
    string = ""
    for l in nodeList[:-1]:
        string += str(l) + ", "
    string += str(nodeList[-1])
    return string

#@stringNode is assumed to be a (name,rank) pair, with name and rank being strings
#@sanitizeNode allows it to be printed "(name,rank)" and not "('name','rank')"
def sanitizeNode(stringNode):
    return "(" + stringNode[0] + "," + stringNode[1] + ")"

#Printing pretty lists of metadata with their default values
def listSampleInvolved(metadataList,interval1List,interval2List,sampleNameList):
    string = ""
    if not metadataList and not interval1List and not interval2List and not sampleNameList:
      print "\n/!\ ERROR: You have selected no sample."
      raise ValueError
    #If samples were selected one by one
    elif sampleNameList:
        string += "\ndepending on the group of samples: "
        for sl in sampleNameList[:-1]:
            string += str(sl) + ", "
        string += str(sampleNameList[-1])
    #If samples were selected according to metadata values (len(metadataList) = len(interval1List) = len(interval2List))
    if metadataList:
        string += "\nselected on metadata (for each line): "
        n = len(metadataList)
        for i in range(n-1):
            if (interval1List[i] == interval2List[i]):
                string += metadataList[i] + " (value equal to " + str(interval1List[i]) + "), "
            else:
                string += metadataList[i] + " (value between " + str(interval1List[i]) + " and " + str(interval2List[i]) + "), "
        if (interval1List[-1] == interval2List[-1]):
            string += metadataList[-1] + " (value equal to " + str(interval1List[-1]) + ")"
        else:
            string += metadataList[-1] + " (value between " + str(interval1List[-1]) + " and " + str(interval2List[-1]) + ")"
    return string

#Selecting samples in two ways: either choose each of them one by one, or selecting according to default values of certain metadatum
def createSampleNameList(dataArray,percentage=False):
    metadataList = []
    interval1List = []
    interval2List = []
    sampleIDList = dataArray[6]
    if percentage:
        i = raw_input("/!\ How many different lists of samples do you want?\n")
        if not integer.match(i):
            print "\n/!\ ERROR: You need to enter a integer here!"
            raise ValueError
        numberList = int(i)
        sampleNameList = []
        if (numberList < 1):
            print "\n/!\ ERROR: Empty set of lists of samples!"
            raise ValueError
        while numberList:
            answer = raw_input("Do you want to select samples one by one, or to select samples matching requirements on metadata? one/matching \n")
            if (answer == "one"):
                if (len(sampleIDList) < 2):
                    print "\n/!\ ERROR: List of samples is empty or only of length one!..."
                    raise ValueError
                print sampleIDList
                sampleNameList11 = parseList(raw_input("Input the list of samples using the ID printed above. [e.g. " + sampleIDList[0] + ";"+ sampleIDList[1] + " ]\n"))
            elif (answer == "matching"):
                print dataArray[1]
                metadataList = parseList(raw_input("Input the list of metadata you want to consider among those written above. [ e.g. " + dataArray[1][0] + ";" + dataArray[1][-1] + " ]\n"))
                isInDatabase(metadataList,dataArray[1])
                interval1List = parseIntList(raw_input("Input the list of lower interval bounds corresponding to metadatum/metadata above. [ Please refer to README for more details. e.g. 1;2 ]\n"))
                if not (len(interval1List) == len(metadataList)):
                    print "\n/!\ ERROR: You need to enter the same number of lower bounds than of metadata!"
                    raise ValueError
                interval2List = parseIntList(raw_input("Input the list of upper interval bounds corresponding to metadatum/metadata above. [ Please refer to README for more details. e.g. 3;2 ]\n"))
                if not (len(interval2List) == len(metadataList)):
                    print "\n/!\ ERROR: You need to enter the same number of upper bounds than of metadata!"
                    raise ValueError
                sampleNameList11 = computeSamplesInGroup(dataArray[0],dataArray[1],metadataList,interval1List,interval2List)[0]
            else:
                print "\n/!\ ERROR: You need to answer either 'one' or 'matching' and not: \"",answer,"\"."
                raise ValueError
            isInDatabase(sampleNameList11,sampleIDList)
            sampleNameList.append(sampleNameList11)
            numberList -= 1
    else:
            answer = raw_input("Do you want to select samples one by one, or to select samples matching requirements on metadata? one/matching \n")
            if (answer == "one"):
                if (len(sampleIDList) < 2):
                    print "\n/!\ ERROR: List of samples is empty or only of length one!..."
                    raise ValueError
                print sampleIDList
                sampleNameList = parseList(raw_input("Input the list of samples using the ID printed above. [e.g. " + sampleIDList[0] + ";"+ sampleIDList[1] + " ]\n"))
            elif (answer == "matching"):
                print dataArray[1]
                metadataList = parseList(raw_input("Input the list of metadata you want to consider among those written above. [ e.g. " + dataArray[1][0] + ";" + dataArray[1][-1] + " ]\n"))
                isInDatabase(metadataList,dataArray[1])
                interval1List = parseIntList(raw_input("Input the list of lower interval bounds corresponding to metadatum/metadata above. [ Please refer to README for more details. e.g. 1;-inf;3 ]\n"))
                if not (len(interval1List) == len(metadataList)):
                    print "\n/!\ ERROR: You need to enter the same number of lower bounds than of metadata!"
                    raise ValueError
                interval2List = parseIntList(raw_input("Input the list of upper interval bounds corresponding to metadatum/metadata above. [ Please refer to README for more details. e.g. +inf;2;1 ]\n"))
                if not (len(interval2List) == len(metadataList)):
                    print "\n/!\ ERROR: You need to enter the same number of upper bounds than of metadata!"
                    raise ValueError
                sampleNameList = computeSamplesInGroup(dataArray[0],dataArray[1],metadataList,interval1List,interval2List)[0]
            else:
                print "\n/!\ ERROR: You need to answer either 'one' or 'matching' and not: \"",answer,"\"."
                raise ValueError
            isInDatabase(sampleNameList,sampleIDList)
    return sampleNameList,metadataList,interval1List,interval2List

#____________________________________________________________________________

#See featuresVector.py and README for more details about features vectors.
def userNodeSelectionAct(dataArray):
    print dataArray[1]
    metadatum = sanitize(raw_input("Input the metadatum that will cluster the set of samples among those written above. [ e.g. " + dataArray[1][0] + " ]\n")).split(";")[0]
    isInDatabase([metadatum],dataArray[1])
    nodesList = parseListNode(raw_input("Choose the group of nodes you want to consider exclusively. [ Read the taxonomic tree to help you: e.g. " + sanitizeNode(dataArray[4][-3]) + ";" + sanitizeNode(dataArray[4][1]) + ";" + sanitizeNode(dataArray[4][-1]) + " ]\n"))
    isInDatabase(nodesList,dataArray[4])
    assignedClasses,classes,valueSet = classifyIt(dataArray,metadatum,nodesList)
    numberClass = len(classes)
    #len(dataArray[0])?
    youdenJ = countYouden(assignedClasses,classes,len(dataArray[0]))
    interpretIt(youdenJ)
    answer = raw_input("Do you want to plot the classes obtained as a pie? Y/N")
    if answer == "Y":
        labelsAs = [ metadatum + " = " + str(value) for value in valueSet ]
        percentagesAs = [ len(class1) for class1 in assignedClasses ]
        labels = [ metadatum + " = " + str(value) for value in valueSet ]
        percentages = [ len(class1) for class1 in classes ]
        plotPie(labelsAs,percentagesAs,"Assignments depending on " + str(nodesList) + " to class for metadatum " + metadatum)
        plotPie(labels,percentages,"Real classes depending on " + str(nodesList) + " for metadatum " + metadatum)
    elif not (answer == "N"):
        print "\n Answer by Y or N!"
    answer = raw_input("Do you want to save the results? Y/N")
    if (answer == "Y"):
        writeFile("Youden's J statistic for this classification is: " + str(youdenJ) + "\n","Assignments depending on " + str(nodesList) + " to classes for metadatum " + metadatum)
    elif not (answer == "N"):
        print "\n Answer by Y or N!"
    return assignedClasses,youdenJ

#________________________________________________________________________________________________________________________

def randomSubSamplingAct(dataArray):
    print dataArray[1]
    metadatum = sanitize(raw_input("Input the metadatum that will cluster the set of samples among those written above. [ e.g. " + dataArray[1][0] + " ]\n")).split(";")[0]
    isInDatabase([metadatum],dataArray[1])
    s = raw_input("Input the number s of random samplings.")
    n = raw_input("Input the number n of nodes to select at each try.")
    if not integer.match(s) or not integer.match(n):
        print "\n/!\ ERROR: s and n must both be integers."
        raise ValueError
    s,n = int(s),int(n)
    #Here the set of classes is a list of two lists containing the samples in C and not C
    bestClassification = []
    bestClassesList = []
    #Worse value for this coefficient
    currBestYouden = inf
    nodesNumber = dataArray[3]
    while s:
        #Randomly draw n distinct nodes among the nodes in the taxonomic tree
        nodesList = randomChoice(dataArray[4],n)
        assignedClasses,classes,valueSet = classifyIt(dataArray,metadatum,nodesList)
        numberClass = len(classes)
        #len(dataArray[0])?
        youdenJ = countYouden(assignedClasses,classes,len(dataArray[0]))
        res = numberClass - youdenJ
        if min(res,currBestYouden) == res:
            bestClassification = []
            for i in nodesList:
                bestClassification.append(i)
            currBestYouden = res
            bestClassesList = []
            for i in assignedClasses:
                bestClassesList.append(i)
        s -= 1
    interpretIt(numberClass - currBestYouden)
    if answer == "Y":
        labelsAs = [ metadatum + " = " + str(value) for value in valueSet ]
        percentagesAs = [ len(class1) for class1 in assignedClasses ]
        labels = [ metadatum + " = " + str(value) for value in valueSet ]
        percentages = [ len(class1) for class1 in classes ]
        plotPie(labelsAs,percentagesAs,"Assignments depending on " + str(nodesList) + " to class for metadatum " + metadatum)
        plotPie(labels,percentages,"Real classes depending on " + str(nodesList) + " for metadatum " + metadatum)
    answer = raw_input("Do you want to save the results? Y/N")
    if (answer == "Y"):
        writeFile("Best Youden's J statistic for this classification is: " + str(numberClass - currBestYouden) + "\nand most relevant list of nodes for this metadatum is:" + str(bestClassification),"Assignments to classes for metadatum " + metadatum)
    elif not (answer == "N"):
        print "\n Answer by Y or N!"
    return bestClassification,(numberClass - currBestYouden),bestClassesList
