execfile('./functionDefinition.py')
execfile('./dbPediaInterface.py')

# Third party libraries
import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
# from nltk.tokenize.punkt import PunktWordTokenizer
# import nltk.tokenize.punkt
from SPARQLWrapper import SPARQLWrapper, JSON

filename = 'GC_Test_Not_Solved_100.xml'
dictQueries = xmlToDict(filename)
##print dictQueries.keys()

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
            
# Tokenize queries
tokenizedQueries = []
for eachQuery in listQueries:
    tokenizedQueries.append(word_tokenize(eachQuery.lower()))

# POS tagging of queries
taggedTokenizedQueries = []
for eachTokenizedQuery in tokenizedQueries:
    taggedTokenizedQueries.append(pos_tag(eachTokenizedQuery))
    
# Search candidate words
candidateLocationsFirstIter = []
for eachTaggedQuery in taggedTokenizedQueries:
    tempCandidateLocation = []
    for token, pos in eachTaggedQuery:
##        if (pos == 'NNP' or pos == 'NN' or pos == 'IN' or pos == 'CD'):
            tempCandidateLocation.append(token)
    candidateLocationsFirstIter.append(tempCandidateLocation)
##print candidateLocationsFirstIter
        
# Create bi grams and trigrams from each candidate word list
nGramCandidateLocation = []
for eachItem in candidateLocationsFirstIter:
    tempNGram = []
    tempNGram = findNgram(eachItem)
    nGramCandidateLocation.append(tempNGram)
##print nGramCandidateLocation
    
'''
Find if the query is local. If a location term is found, then query is said to be local.
'''
# Search nGrams in dbPedia for match
predictedLocation = []
for eachListItem in nGramCandidateLocation:
    tempPredictedLocation = []
    for each in eachListItem:
##        print each
        if len(each) > 0:
            if not type(each) == str:
##                if len(each) > 1:
                if (isLocation(' '.join(each)) or isCity(' '.join(each)) or isCountry(' '.join(each)) or isRegion(' '.join(each))):
                    tempPredictedLocation.append(' '.join(each))
##                        print (' '.join(each))
##                else:
##                    if (isCity(each) or isCountry(each)):
##                        tempPredictedLocation.append(each)
            else:
                if (isLocation(each) or isCity(each) or isCountry(each) or isRegion(each)):
                    tempPredictedLocation.append(each)
        else:
##            print each            
            tempPredictedLocation.append([])
    predictedLocation.append(tempPredictedLocation)
print predictedLocation

# If for a query, more than two locations are predicted, returned the one with maximum number of tokens.
_predictedLocation = []
for eachPredictedLocation in predictedLocation:
##    if len(eachPredictedLocation) > 0:
##        for eachElement in eachPredictedLocation:
        if len(eachPredictedLocation) == 1:
            _predictedLocation.append(eachPredictedLocation[0])
        elif len(eachPredictedLocation) > 1:
            _predictedLocation.append(eachPredictedLocation[-1])
        elif len(eachPredictedLocation) == 0:
            _predictedLocation.append('NA')
                
# If query contains a location term, then refer the query as a local query.
isLocalQuery = []
for _PredictedLocation in _predictedLocation:
    if _PredictedLocation != 'NA':
        isLocalQuery.append('YES')
    else:
        isLocalQuery.append('NO')
    
'''
Find geo-relation word. First find candidate relation type words for each query. Then match those with the pre defined relation types given in project description.
'''
# Get index of location term from the list of tokens
candidateRelationWords = []
indexOfLocationInTokens = []
for i in range(len(_predictedLocation)):
    if _predictedLocation[i] == 'NA':
        indexOfLocationInTokens.append('NA')
    else:
        # Check if the predicted location consists of two or more tokens. If yes, return the index of the first token in the tokenizedQueries
        if ' ' in _predictedLocation[i]:
            indexOfLocationInTokens.append(tokenizedQueries[i].index(_predictedLocation[i].split()[0]))
        elif not ' ' in _predictedLocation[i]:
            indexOfLocationInTokens.append(tokenizedQueries[i].index(_predictedLocation[i]))
    
# Get candidate words for relation type
candidateRelationTypeWords = []
for j in range(len(tokenizedQueries)):
    if type(indexOfLocationInTokens[j]) == int:
        candidateRelationTypeWords.append(tokenizedQueries[j][0: indexOfLocationInTokens[j]])
    else:
        candidateRelationTypeWords.append('NA')

# Form nGrams from three words prior to the location term in query
nGramsCandidateRelationWords = []
for eachCandidateRelationWord in candidateRelationTypeWords:
    # 'NA' symbolizes that no location term could be found in the query. [] implies that either all the tokens in the query are locations or
    #  location term was found but no candidate relation word could be found before the location term.
    if (len(eachCandidateRelationWord) > 0 and eachCandidateRelationWord == 'NA'):
        # NA_Type_1: No location word found in query. Hence, no relation type word.
        nGramsCandidateRelationWords.append('NA_Type_1')
    elif len(eachCandidateRelationWord) == 0:
        # NA_Type_2: All query tokens combined are location name or location term was found but no candidate relation word could be found before the location term.
        nGramsCandidateRelationWords.append('NA_Type_2')
    else:
        nGramsCandidateRelationWords.append(findNgram(eachCandidateRelationWord))

# Read predefined realtion types from file. 
# Pre defined relation types are in the file in the inputFiles folder
with open('./inputFiles/geoRelationTypeDictionary', 'r') as f:
    listGeoRelationType = f.read().split()

_listGeoRelationType = []
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
Finding the 'WHAT' in the query:
Query sans 'location name' and 'geo relation type' word is the 'WHAT' term.
Step 1: Tokenize the 'location name'and 'geo relation' words.
Step 2: Remove the resulting tokens from the tokenized query one by one.
Step 3: Concatene the resulting tokens to get the WHAT term. List _predictedWhatTerm contains the predicted what terms.
'''
tokensLocation = []
tokensRelationType = []

for elmLoc in range(len(_predictedLocation)):
    tempTokensLocation = []
    if not _predictedLocation[elmLoc] == 'NA':
        tempTokensLocation.append(word_tokenize(_predictedLocation[elmLoc]))
    else:
        tempTokensLocation.append([])
    tokensLocation.append(tempTokensLocation)    

for elmRel in range(len(_geoRelationWord)):
    tempTokensRelationType = []
    if not _geoRelationWord[elmRel] == 'Not Found':
        tempTokensRelationType.append(word_tokenize(_geoRelationWord[elmRel]))
    else:
        tempTokensRelationType.append([])
    tokensRelationType.append(tempTokensRelationType)    

# Unpack list
_tokensLocation = []
for eachInnerList1 in tokensLocation:
	for each1 in eachInnerList1:
		_tokensLocation.append(each1)        

_tokensRelationType = []
for eachInnerList2 in tokensRelationType:
	for each2 in eachInnerList2:
		_tokensRelationType.append(each2)        

# In each tokenizedQuery remove the corresponding tokens from _tokensLocation and _tokensRelationType
whatTermInQueryIterOne = []
for count1 in range(len(_tokensLocation)):
    if _predictedLocation[count1] != 'NA':
        tempSetTokensLocation = set()
        tempResult1 = []
        tempSetTokensLocation = set(_tokensLocation[count1])
        tempResult1 = [x for x in tokenizedQueries[count1] if x not in tempSetTokensLocation]
        whatTermInQueryIterOne.append(tempResult1)
    else:
        whatTermInQueryIterOne.append([])
    
whatTermInQueryIterTwo = []
for count2 in range(len(_tokensRelationType)):
    tempSetRelationType = set()
    tempResult2 = []
    tempSetRelationType = set(_tokensRelationType[count2])
    tempResult2 = [x for x in whatTermInQueryIterOne[count2] if x not in tempSetRelationType]
    whatTermInQueryIterTwo.append(tempResult2)
    
_predictedWhatTerm = []
for eachWhatTerm in whatTermInQueryIterTwo:
    _predictedWhatTerm.append(' '.join(eachWhatTerm))

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
Generate output XML
Following lists shall be used to generate the outout XML:
listQueryNumber, listQueries, isLocalQuery, _predictedWhatTerm, _predictedWhatType, _geoRelationWord, _predictedLocation, _geoCoordinates
'''

# Dummy list of WHAT_TYPE to test if output is generated
i= 100
_predictedWhatType = []
for j in range(i):
	_predictedWhatType.append('WhatType')

toXML(listQueryNumber, listQueries, isLocalQuery, _predictedWhatTerm, _predictedWhatType, _geoRelationWord, _predictedLocation, _geoCoordinates)



