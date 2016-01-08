import xml.etree.ElementTree as ET
import query_reduced_classes as QC

def xmlToQueryList(xmlName):
    tree = ET.parse(xmlName)
    root = tree.getroot()

    xml = root.iter()
    child = next(xml,None)
    q = None
    queries = []
    while child != None:
        if child.tag == 'QUERYNO':
            if q != None:
                queries.append(q)
            q = QC.Query(child.text)
        elif hasattr(q,'_'+child.tag.lower().replace("-","")):
            setattr(q,'_'+child.tag.lower().replace("-",""),child.text)
        elif q != None:
            queries.append(q)
            q = None
        child = next(xml,None)
    return queries
