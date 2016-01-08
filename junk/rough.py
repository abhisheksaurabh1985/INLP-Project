execfile('./dbPediaInterface.py') 

fileCommonEnglishWords= './wordsEn_small.txt'

with open(fileCommonEnglishWords, 'r') as fileObj:
    commonEnglishWords = fileObj.read().split()

commonEnglishWordsSansLocation= []
for eachListItem in commonEnglishWords:
    if not (isCity(eachListItem) or isCountry(eachListItem)):
        commonEnglishWordsSansLocation.append(eachListItem)
    
    
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



