# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import query_classes as QC

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
        elif hasattr(q,'set_'+child.tag.lower().replace("-","")):
            getattr(q,'set_'+child.tag.lower().replace("-","")).im_func(q,child.text)
        elif q != None:
            queries.append(q)
            q = None
        child = next(xml,None)
    return queries
