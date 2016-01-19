from __future__ import division
import sys
package_list = ["xml.etree","collections","geopy","nltk"]
i=0
try:
    from xml.etree import ElementTree
    i+=1
    from collections import OrderedDict
    i+=1
    from geopy.geocoders import Nominatim
    import nltk
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
        return 0, 0

def toXML(listQueryNumber, listQueries, isLocalQuery, _predictedWhatTerm, _predictedWhatType, _geoRelationWord, _predictedLocation, _geoCoordinates):
    toSave = []
    for i in range (0,len(listQueries)):
        if not _geoCoordinates[i]:
            lat = ""; lon = ""
        else:
            m,n = _geoCoordinates[i]
            lat = "%.2f" % m + ", %.2f" % n

        query = l.Query(bytes(listQueryNumber[i]), listQueries[i], isLocalQuery[i], _predictedWhatTerm[i], _predictedWhatType[i], _geoRelationWord[i], _predictedLocation[i],bytes(lat))
        toSave.append(query)
    lf.saveQueriesToXml(toSave,'./output/finalOutput.xml')
#seems to be that listquery number does not have integers, it has lists

def getYellowTerms (file):
    yellowterms = []
    with open(file,"r") as file:
        for line in file:
            yellowterms.append(line.strip("\n"))

        yellow_toks = []
        for elem in yellowterms:
            yellow_toks.extend(nltk.word_tokenize(elem))

        yellow_toks_valid = [elem.lower() for elem in yellow_toks if len(elem) > 2]
        stemmer = nltk.stem.porter.PorterStemmer()
        yellow_stems = [stemmer.stem(elem) for elem in yellow_toks_valid]
        # Only keep unique values
        yellowterms = set(yellow_stems)
    return yellowterms

def checkTokenYellow(tokenizedQuery, yellowterms):
    stemmer = nltk.stem.porter.PorterStemmer()

    for word in tokenizedQuery:
        if stemmer.stem(word) in yellowterms:
            return True
    return False

def filterGeoRelation(query_tokens):

	grammar = r"""
				WHERE: 	<IN.*>+{<DT>?<NN.*>+<.*>*}
				WHERE: 	<IN.*>+{<JJ.*>*<NN.*>+<.*>*}
				WHAT:	{<.*>+}<IN>+<WHERE>
				GEOR:	<WHAT>{<IN>+}<WHERE>
				GEOR:   {<IN>+}<LOC>
				"""

	cp = nltk.RegexpParser(grammar)
	res = cp.parse(query_tokens)
	return res

def getGeoTriplet(result):
    where = []
    what = []
    geo = []
    cards = ['east','west','north','south','northeast','northwest','southeast','southwest']
    for n in result:
        if isinstance(n, nltk.tree.Tree):
            nn = [''.join(w) for (w,p) in n.leaves()]
            if 'WHERE' in n.label():
                where.extend(nn)
            if 'WHAT' in n.label():
                what.extend(nn)
            if 'GEO' in n.label():
                geo.extend(nn)
    if what:
        if what[-1] in cards:
            #[what[-1]].extend(geo)
            geo = [what[-1]+' '+' '.join(geo)]
            what = what[0:-1]

    return where, geo, what;


coordinates = ['north','south','west','east','northwest','northeast','southwest','southeast']
geocords = ['NORTH_OF','SOUTH_OF','WEST_OF','EAST_OF','NORTH_WEST_OF','NOTRH_EAST_OF','SOUTH_WEST_OF','SOUTH_EAST_OF']