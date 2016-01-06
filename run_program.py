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

# Extract proper nouns

# Words to be discarded while searching location names
with open('./commonnounlist.txt', 'r') as fileObj1:
    commonNounWords = fileObj1.read().split()

with open('./wordsEn.txt', 'r') as fileObj2:
    commonEnglishWords = fileObj2.read().split()

# Common English words contain some location names. For e.g. america, england etc. These words will have to removed from this list. The resulting list shall be used to filter
# out the words from the tagged queries.
with open('./prominentLocationNames.txt', 'r') as fileObj3:
    prominentLocationNames = fileObj3.read().split()
# Change location names to lower case
prominentLocationNames = [element.lower() for element in prominentLocationNames]

# Get set difference between commonEnglishWords and prominentLocationNames
_commonEnglishWords = list(set(commonEnglishWords).difference(set(prominentLocationNames)))
ignoreWords = commonNounWords + _commonEnglishWords

# Stemming of the words to be discarded
commonNounWordsStemmed = []
porter_stemmer = PorterStemmer()
for eachCommonNounWord in commonNounWords:
    commonNounWordsStemmed.append(porter_stemmer.stem(eachCommonNounWord))

commonEnglishWordsStemmed = []
for eachCommonEnglishWord in commonEnglishWords:
    commonEnglishWordsStemmed.append(porter_stemmer.stem(eachCommonEnglishWord))

ignoreWordsStemmed = []
for eachIgnoreWords in ignoreWords:
    ignoreWordsStemmed.append(porter_stemmer.stem(eachIgnoreWords))

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
    # 'NA' symbolizes that no location term could be found in the query. [] implies that all the tokens in the query are locations and no candidate relation word could be obtained.
    if (len(eachCandidateRelationWord) > 0 and eachCandidateRelationWord == 'NA'):
        # NA_Type_1: No location word found in query. Hence, no relation type word.
        nGramsCandidateRelationWords.append('NA_Type_1')
    elif len(eachCandidateRelationWord) == 0:
        # NA_Type_2: All query tokens combined are location name.
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
            if eachInnerListItem in _listGeoRelationType:
                tempGeoRelation.append(eachInnerListItem)
##            else:
##                # NA_Type_3 : No geo relation type in the query though it is has a location term
##                tempGeoRelation.append('NA_Type_3')
    geoRelationWord.append(tempGeoRelation)                

# In case for a query we get multiple geo relation type words, retain the last one. Considering that the word just before Location name has a higher probability of defining geo relation.
_geoRelationWord = []
for m in range(len(geoRelationWord)):
    if not len(geoRelationWord[m]) == 0:
            for n in range(len(geoRelationWord[m])):
                if geoRelationWord[m][n] == 'NA_Type_1' or geoRelationWord[m][n] == 'NA_Type_2':
                    _geoRelationWord.append('Not Found')
                else:
                    _geoRelationWord.append(geoRelationWord[m][-1])
    else:
        _geoRelationWord.append('Not Found')
        
        

