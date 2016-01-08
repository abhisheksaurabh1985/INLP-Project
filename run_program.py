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

filename = 'GC_Tr_100.xml'
dictQueries = xmlToDict(filename)
##print dictQueries.keys()

# Iterate over the dictionary and save the queries in a list
listQueries = []
for keyOuter, valuesOuter in dictQueries.iteritems():
    for keyInner, valuesInner in valuesOuter.iteritems():
        if keyInner == 'QUERY':
            listQueries.append(valuesInner)

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
        if (pos == 'NNP' or pos == 'NN' or pos == 'IN' or pos == 'CD'):
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

################################################################################
# Match candidate relation type words with the pre defined relation types given
################################################################################
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
Step 1: Tokenize the 'location name' and 'geo relation type'.
Step 2: Combine the two tokens and make a set.
Step 3: Take the set difference with the tokenized query and convert the resulting set to list.
Step 4: Join the list items. Result would be the 'WHAT' term in the queries.
'''
whatTermInQuery = []
tokensLocation = []
tokensRelationType = []
for elm in range(len(_predictedLocation)):
    tempTokensLocation = []
    tempTokensRelationType = []
    if (not _predictedLocation[elm]  == 'NA' and not _geoRelationWord[elm] == 'Not Found'):
        tempTokensLocation.append(word_tokenize(_predictedLocation[elm]))
        tempTokensRelationType.append(word_tokenize(_geoRelationWord[elm]))
    else:
        tempTokensLocation.append([])
        tempTokensRelationType.append([])
    tokensLocation.append(tempTokensLocation)
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

# Merge list of tokens and relation types
