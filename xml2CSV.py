# Corpus accessor for accessing .xml file. Output of this accessor shall be a more suitable
# representation of the queries. Accessor would access both the training and the test dataset.

# ElementTree library has been used  to parse the XML documents. It is a part of the Python standard library.

# Import the required library
import xml.etree.ElementTree as etree

# Read file
fileName = etree.parse('./GC_Test_Not_Solved_100.xml')

# Find root and its sub elements
root=fileName.getroot()

# Print the name of sub elements and the text associated with each sub-element
childName = [] # Empty list. To be populated with the names of the 'child' element
childText = [] # Empty list. To be populated with text associated with each 'child' element within the 'root' element

# Populate the childName and childText empty lists
for child in root:
    childName.append(child.tag)
    childText.append(child.text)

# Get unique child elements while preserving the order in which they exist in the original list
def getUniqueChildElements(inputList):
    uniqueElements = []
    for listElement in inputList:
        if listElement not in uniqueElements:
            uniqueElements.append(listElement)
    return uniqueElements

# Divide the list containing the text corresponding to sub-elements into multiple list with size of each of those being a multiple of the number of Columns
def getChunks(inputSubElementTextList, nColumn):
    n = max(1,nColumn)
    return[inputSubElementTextList[i:i+nColumn]for i in range(0, len(inputSubElementTextList),nColumn)]
    
# Get number of sets of child elements by counting the number of occurrences of QueryNo. Input the list containing the names of the child element
def getCountQueries(inputList):
    dictionaryQueryElements = {x:inputList.count(x) for x in inputList}
    listOfValues = list(dictionaryQueryElements.values())
    numberQueries = listOfValues[1]
    return numberQueries

# Two dimensional spreadsheet representation of queries
def getSpreadsheetRepresentation(inputListElementName, inputListElementText):
    numberColumns = len(getUniqueChildElements(inputListElementName))
    numberRows = getCountQueries(inputListElementName)
    # Create an empty two dimensional list
    spreadsheetRepresentationQueries = []
    # Populate the empty list with headers of the spreadsheet
    spreadsheetRepresentationQueries.append(getUniqueChildElements(inputListElementName))
    # Divide the list containing the text corresponding to sub-elements into multiple list with size of each of those being a multiple of the number of Columns
    subElementText = getChunks(inputListElementText, numberColumns)
    for i in range(len(subElementText)):
        spreadsheetRepresentationQueries.append(subElementText[i])
    return spreadsheetRepresentationQueries
    
# Commands to test the code
print(childName)
print("\n\n",childText)

# Obtain the headers of the CSV
headersCSV= getUniqueChildElements(childName)
print("\n\n",headersCSV)

# Obtain number of columns
numberColumns = len(getUniqueChildElements(childName))
print("\n\n",numberColumns)

# Obtain number of queries
numberQueries= getCountQueries(childText)
print("\n\n",numberQueries)

# Obtain chunks of queries
queriesInChunks= getChunks(childText, numberColumns)
print("\n\n",queriesInChunks)

# Obtain spreadsheet representation of queries
queriesInTwoDimList = getSpreadsheetRepresentation(childName, childText)
print("\n\n",queriesInTwoDimList)
            
# Obtain CSV file from the nested list    
import csv
data = getSpreadsheetRepresentation(childName, childText)
with open('queriesInSpreadsheet.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter= ',')
    writer.writerows(data)
    csvfile.close()
    


