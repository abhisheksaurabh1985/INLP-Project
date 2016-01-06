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
        if len(eachPredictedLocation) == 0:
            _predictedLocation.append([])
        elif len(eachPredictedLocation) == 1:
            _predictedLocation.append(eachPredictedLocation)
        elif len(eachPredictedLocation) > 1:
            _predictedLocation.append(eachPredictedLocation[-1])
        
#             
    
    
