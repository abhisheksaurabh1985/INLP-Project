from xml.etree import ElementTree
from collections import OrderedDict

def xmlToDict(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()
 
    dictQueries = OrderedDict()
    for i in range(len(root)):
        
        if root[i].tag=='QUERYNO':
            idDict = int(root[i].text)
            dictQueries[idDict]= OrderedDict()
        else:
            dictQueries[idDict][root[i].tag] = root[i].text
    return dictQueries

# Find bigrams and trigrams from an input list of words
def findNgram(listWords):
    ngramList = []
    unigramList = []
    bigramList = []
    trigramList = []
    # Find unigrams
    for i in range(len(listWords)):
        unigramList.append((listWords[i]))
    # Find bigrams
    for i in range(len(listWords)-1):
        bigramList.append((listWords[i], listWords[i+1]))
    # Find trigrams
    for i in range(len(listWords)-2):
        trigramList.append((listWords[i], listWords[i+1], listWords[i+2]))
    # Append bigrams and trigrams in single list
    ngramList = unigramList + bigramList + trigramList
    return(ngramList)



