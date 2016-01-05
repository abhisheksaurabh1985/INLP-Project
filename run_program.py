execfile('./functionDefinition.py')
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
import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
# from nltk.tokenize.punkt import PunktWordTokenizer
# import nltk.tokenize.punkt

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

print(candidateLocationsFirstIter)
        
    
# Create bi grams and trigrams
# Search dbPedia for macth




# Stem the tokens. Search the stemmed tokens in the stemmed commonNounWords and _commonEnglishWords list. If search is not found, return the original token.

##predictedCandidateLocationName = []
##listStemmedAllQueryTokens = []
##for eachTaggedQuery in taggedTokenizedQueries:
##    currentLocationWords = []
##    listStemmedQueryTokens = []
##    for token, pos in eachTaggedQuery:
##        listStemmedQueryTokens.append(porter_stemmer.stem(token))
##    listStemmedAllQueryTokens.append(listStemmedQueryTokens)
##
### Predict candidate words for location
##for i in range(len(listStemmedAllQueryTokens)):
##    for j in range(len(listStemmedAllQueryTokens[i])):
##        if listStemmedAllQueryTokens[i][j] not in commonNounWordsStemmed:
##            candidateLocationWords.append(taggedTokenizedQueries[i][j])
##        else:
##            candidateLocationWords.append([])
##            
##print candidateLocationWords            
        

        
##        # print token
####          if (token.lower() not in commonNounWords):
####             print token.lower()
##        if token.lower() not in ignoreWords:
##            print token
##            if pos =='NNP' or pos== 'NN':
##                currentCandidate.append(token)
##            #     continue
##            # if len(currentCandidate)> 0:
##            #     print ' '.join(currentCandidate)
##    # if len(currentCandidate)>0:
##        # print ' '.join(currentCandidate)
##    predictedCandidateLocationName.append(currentCandidate)
##
##print predictedCandidateLocationName


### Ninety one thousand nouns
##with open('./91K nouns.txt', 'r') as fileObj2:
##    ninetyOneKNouns = fileObj2.read().split()
##
### Read list of countries and prominent cities
##with open('./prominentLocationNames.txt', 'r') as fileObj3:
##    prominentLocationNames = fileObj3.read().split()
##
### Remove prominent location names from ninety one thousand nouns
##
