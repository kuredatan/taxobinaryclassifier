import matplotlib.pyplot as plt
import numpy as np

#@labels is the array containing the labels of the pie (can go up to 14 different labels)
#@sizes is the arrays of parts of the pie owned by the different labels
def plotPie(labels,sizes,title):
    initColors = ['gold','yellowgreen','lightcoral','lightskyblue','violet','blue','pink','red','orange','green','gray','black','brown','yellow']
    n = len(labels)
    if not (n == len(sizes)):
        print "\n/!\ ERROR: Different lengths ",len(labels),"and",len(sizes)
        raise ValueError
    if n > 14:
        print "\n/!\ ERROR: Not enough colors! Please modify plottingValues.py and restart Python"
        raise ValueError
    #explode maximum percentage
    iMax = 0
    maximum = 0
    for i in range(n):
        if maximum < sizes[i]:
            iMax = i
            maximum = sizes[i]
    explode = [0] * n
    explode[iMax] = 0.1
    labels = labels
    sizes = sizes
    colors = initColors[:n]
    plt.pie(sizes,explode=explode,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=140)
    plt.axis('equal')
    plt.title(title)
    plt.show()
