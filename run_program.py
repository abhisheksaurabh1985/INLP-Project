execfile('./functionDefinition.py')
execfile('./dbPediaInterface.py')

# Third party libraries

import nltk

from nltk.tag import pos_tag
import scorer


filename = 'GC_Tr_100_small.xml'
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

tokenizedQueries = [nltk.word_tokenize(eachQuery.lower()) for eachQuery in listQueries]
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
for eachPredictedLocation in predictedLocation: #if what empty meter en what el resto
    if len(eachPredictedLocation) == 1:
        _predictedLocation.append(eachPredictedLocation[0])
    elif len(eachPredictedLocation) > 1:
        _predictedLocation.append(eachPredictedLocation[-1])
    elif len(eachPredictedLocation) == 0:
        _predictedLocation.append('NA')

for i in range(len(predictedLocation)):
    if not predictedWhat[i]:
        pos = predictedWhere[i].index(_predictedLocation[i])
        predictedWhat[i] = predictedWhere[i][0:pos]
        _predictedLocation[i] = ' '.join(predictedWhere[i][pos:])

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

'''_listGeoRelationType = []
for eachGeoRelation in listGeoRelationType:
    if ('_' in eachGeoRelation):
        _listGeoRelationType.append(eachGeoRelation.replace("_", " "))
    else:
        _listGeoRelationType.append(eachGeoRelation)

# Match candidate relation words with the dictionary of relation words
geoRelationWord = []
for eachNGramCandidateRelation in nGramsCandidateRelationWords:
    tempGeoRelation = []
    if eachNGramCandidateRelation == 'NA_Type_1':
        tempGeoRelation.append('NA_Type_1')
    elif eachNGramCandidateRelation == 'NA_Type_2':    
        tempGeoRelation.append('NA_Type_2')
    else:
        for eachInnerListItem in eachNGramCandidateRelation:
            if type(eachInnerListItem) == str:
                if eachInnerListItem in _listGeoRelationType:
                    tempGeoRelation.append(eachInnerListItem)
            elif type(eachInnerListItem) == tuple:
                if ' '.join(eachInnerListItem) in _listGeoRelationType:
                    tempGeoRelation.append(' '.join(eachInnerListItem))
    geoRelationWord.append(tempGeoRelation)                

# In case for a query we get multiple geo relation type words, retain the last one. Considering that the word just before Location name has a higher probability of defining geo relation.
_geoRelationWord = []
for m in range(len(geoRelationWord)):
    if not len(geoRelationWord[m]) == 0:
        if geoRelationWord[m][0] == 'NA_Type_1' or geoRelationWord[m][0] == 'NA_Type_2':
            _geoRelationWord.append('Not Found')
        else:
            _geoRelationWord.append(geoRelationWord[m][-1])
    else:
        _geoRelationWord.append('Not Found')
'''

'''
Latitude and Longitude of a place. Python module Geopy has been used to get the coordinates of a location.
'''
_geoCoordinates = []
for _everyPredictedLocation in _predictedLocation:
    if _everyPredictedLocation != 'NA':
        _geoCoordinates.append(getCoordinates(_everyPredictedLocation))
    else:
        _geoCoordinates.append('')
    
# Round the geo coordinates to 2 digits and format it as '40.23,<space>-75.30'
_geoCoordinatesRounded = []
for _eachGeoCoordinate in _geoCoordinates:
    if _eachGeoCoordinate != '':
        tempEachGeoCoordinate = []
        for eachCoordinate in _eachGeoCoordinate:
            eachCoordinate = round(eachCoordinate, 2)
            tempEachGeoCoordinate.append(eachCoordinate)
        _geoCoordinatesRounded.append(tempEachGeoCoordinate)   
    else:
        _geoCoordinatesRounded.append('')

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


toXML(listQueryNumber, listQueries, isLocalQuery, _predictedWhat, _predictedWhatType, _predictedGeo , _predictedLocation, _geoCoordinates)

precission, recall, fi = scorer.score("output/finalOutput.xml","GC_Tr_100_small.xml")

print precission,recall,fi