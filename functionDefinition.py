from __future__ import division
import sys
package_list = ["xml.etree","collections","geopy"]
i=0
try:
    from xml.etree import ElementTree
    i+=1
    from collections import OrderedDict
    i+=1
    from geopy.geocoders import Nominatim
except ImportError:
    print("\nERROR: Module " + package_list[i] + " is not installed")
    print("INFO: Use \"pip install "+package_list[i]+"\" to install it and try to run the program again\n")
    sys.exit(1)


import labo_classes as l
import labo_functions as lf


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

def comparePredictions(predictIsLocal, actIsLocal, predictWhat, actWhat, predictWhatType, actWhatType, predictGeoRelation,
                       actGeoRelation, actWhere, predictWhere ):
    #This function returns a tuple (correctlyTaggedQueries, predictionResults)
    predictionResults = []
    correctlyTaggedQueries = 0
    for i in range(0,len(predictIsLocal)):

        if (predictIsLocal[i] == actIsLocal[i]) & (predictWhat[i] == actWhat[i]) & (predictWhatType[i] == actWhatType[i])\
                &(predictGeoRelation[i] == actGeoRelation[i]) & (actWhere[i] == predictWhere[i]):
            predictionResults.append('1')
            correctlyTaggedQueries+= 1
        else:
            predictionResults.append('0')


    return correctlyTaggedQueries, predictionResults

def getMetrics (correctlyTaggedQueries, predictionResults, totalQueries, totalLocalQueries):
    precision = correctlyTaggedQueries / totalQueries
    recall = correctlyTaggedQueries / totalLocalQueries
    f1Score = 2* precision* recall / (precision + recall)

    return precision, recall, f1Score

def getCoordinates (location):
    try:
        geolocator = Nominatim()
        location = geolocator.geocode(location)
        return location.longitude, location.latitude
    except AttributeError:
        print 'NoneType: object has no attribute longitude'
        return '', ''
        return None

def toXML(listQueryNumber, listQueries, isLocalQuery, _predictedWhatTerm, _predictedWhatType, _geoRelationWord, _predictedLocation, _geoCoordinates):
    toSave = []
##    print _geoRelationWord
    for i in range (0,len(listQueries)):
        coords = ','.join(str(_geoCoordinates[i]))
##        print coords
        toSave.append(l.Query(bytes(i), listQueryNumber[i], listQueries[i], isLocalQuery[i], _predictedWhatTerm[i], _predictedWhatType[i], _geoRelationWord[i], _predictedLocation[i],coords))
    lf.saveQueriesToXml(toSave,'./output/finalOutput.xml')


def getYellowTerms (file):
    yellowterms = []
    with open(file,"r") as file:
        for line in file:
            yellowterms.append(line.strip("\n"))
    return yellowterms

def checkTokenYellow(tokenizedQuery, yellowterms):
    for word in tokenizedQuery:
        if word in yellowterms:
            return True
    return False
