from misc import truncate

def countYouden(classesList,metadataList):
    ()

def interpretIt(youdenJ):
    if youdenJ > 1 or youdenJ < -1:
        print "\n/!\ ERROR: Youden's index must be comprised between -1 and 1."
        raise ValueError
    elif youdenJ == 1:
        print "Perfect correlation between the metadata selected and the phylogeny."
    elif youdenJ < 1 and 0.5 < youdenJ:
        print "1"
    elif youdenJ <= 0.5 and 0 < youdenJ:
        print "2"
    elif youdenJ == 0:
        print "Useless test."
    elif youdenJ < 0 and -0.5 <= youdenJ:
        print "3"
    else:
        print "4"
