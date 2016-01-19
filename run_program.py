execfile('./functionDefinition.py')
execfile('./dbPediaInterface.py')

# Third party libraries

import nltk

from nltk.tag import pos_tag
import scorer

print 'Parsing XML File'
filename = 'GC_Tr_100.xml'
dictQueries = xmlToDict(filename)

# Iterate over the dictionary and save the queries in a list
listQueries = []
for keyOuter, valuesOuter in dictQueries.iteritems():
    for keyInner, valuesInner in valuesOuter.iteritems():
        if keyInner == 'QUERY':
            listQueries.append(valuesInner)

# Iterate over the dictionary and save the query numbers in a list
listQueryNumber = []
for kOuter, valOuter in dictQueries.iteritems():
        listQueryNumber.append(kOuter)

print 'Tokenizing Queries'
tokenizedQueries = [nltk.word_tokenize(eachQuery.lower()) for eachQuery in listQueries]
print 'Applying POS-TAGGER'
taggedTokenizedQueries = [pos_tag(eachTokenizedQuery) for eachTokenizedQuery in tokenizedQueries]
solution = []
predictedWhere = []
predictedGeo = []
predictedWhat = []
for query,notagged in zip(taggedTokenizedQueries,tokenizedQueries):
    result = filterGeoRelation(query)
    where, geo, what = getGeoTriplet(result)
    if not where: where = notagged;
    predictedWhere.append(where)
    predictedGeo.append(geo)
    predictedWhat.append(what)

# Create bi grams and trigrams from each candidate word list
nGramCandidateLocation = []
for eachItem in predictedWhere:
    tempNGram = []
    tempNGram = findNgram(eachItem)
    nGramCandidateLocation.append(tempNGram)

'''
Find if the query is local. If a location term is found, then query is said to be local.
'''
print 'Querying DBpedia. . .'
# Search nGrams in dbPedia for match
predictedLocation = []
for eachListItem in nGramCandidateLocation:
    tempPredictedLocation = []
    for each in eachListItem:
        if len(each) > 0:
            if not type(each) == str:
                tmp = ' '.join(each)
                if (isLocation(tmp) or isCity(tmp) or isCountry(tmp) or isRegion(tmp)):
                    tempPredictedLocation.append(tmp)
            else:
                if (isLocation(each) or isCity(each) or isCountry(each) or isRegion(each)):
                    tempPredictedLocation.append(each)
        else:
            tempPredictedLocation.append([])
    predictedLocation.append(tempPredictedLocation)

# If for a query, more than two locations are predicted, returned the one with maximum number of tokens.
_predictedLocation = []
for eachPredictedLocation in predictedLocation:
    if len(eachPredictedLocation) == 1:
        _predictedLocation.append(eachPredictedLocation[0])
    elif len(eachPredictedLocation) > 1:
        _predictedLocation.append(eachPredictedLocation[-1])
    elif len(eachPredictedLocation) == 0:
        _predictedLocation.append('NA')

for i in range(len(_predictedLocation)):
    if (predictedWhat[i]) or (_predictedLocation[i] != 'NA'):
        tmp  =' '.join(predictedWhere[i])
        loc = ' '.join(predictedLocation[i])
        predictedWhat[i] = [tmp.strip(loc)]
    if (_predictedLocation[i]!= 'NA'):
        predictedWhere[i] = ""
    for j in range(len(predictedWhat[i])):
        if tmp[j] in coordinates:
            indx = coordinates.index(tmp[j])
            predictedWhat[i] = predictedWhat[0:j]
            predictedGeo[i] = geocords[indx]


# If query contains a location term, then refer the query as a local query.
isLocalQuery = []
for _PredictedLocation in _predictedLocation:
    if _PredictedLocation != 'NA':
        isLocalQuery.append('YES')
    else:
        isLocalQuery.append('NO')

# Read predefined realtion types from file. 
# Pre defined relation types are in the file in the inputFiles folder
#with open('./inputFiles/geoRelationTypeDictionary', 'r') as f:
#    listGeoRelationType = f.read().split()



'''
Latitude and Longitude of a place. Python module Geopy has been used to get the coordinates of a location.
'''
_geoCoordinates = []
for _everyPredictedLocation in _predictedLocation:
    if _everyPredictedLocation != 'NA':
        _geoCoordinates.append(getCoordinates(_everyPredictedLocation))
    else:
        _geoCoordinates.append('')

'''
Determination of WHAT TYPE:
If number of tokens in a query is equal to the number of tokens in the corresponding location, then query is of type MAP. 
'''
_predictedWhatType = []
yellowTerms = getYellowTerms('./terms')


for what in predictedWhat:
    if not what:
        _predictedWhatType.append('MAP')
    elif checkTokenYellow(what,yellowTerms):
        _predictedWhatType.append('Yellow page')
    else:
        _predictedWhatType.append('Information')


'''
Generate output XML

'''
_predictedWhat = []
for list in predictedWhat:
    _predictedWhat.append(','.join(list).replace(','," "))

_predictedGeo = []
for sublist in predictedGeo:
    if not sublist:
        _predictedGeo.append("")
    for val in sublist:
        _predictedGeo.append(val.upper())

for i in range(len(_predictedLocation)):
    if _predictedLocation[i] == 'NA':
        _predictedLocation[i] = ""


toXML(listQueryNumber, listQueries, isLocalQuery, _predictedWhat, _predictedWhatType, _predictedGeo , _predictedLocation, _geoCoordinates)

precission, recall, fi = scorer.score("output/finalOutput.xml","GC_Tr_100.xml")

print precission,recall,fi