#!/usr/bin/python
#-----------------------------------------------------------------------------
#
# Author: Group-5 (Khalid, Immanuel, Marco)
#
#
# A python Interface for accessing DBPedia in order
# to check whether a string could correspond  to a
# location (a city, a country, a state, etc).
#
#-----------------------------------------------------------------------------

from SPARQLWrapper import SPARQLWrapper, JSON

target = "http://dbpedia.org/sparql"
sparql = SPARQLWrapper(target)

def normalize(term):
    """
    Capitalize each word of the string and check for spaces
    and convert them into underscores (_).
    Example: mount everest --> Mount_Everest
             barcelona     --> Barcelona
    term
        string to capitalize
    return
        the string capitalized as explained above
    """

    t = term.title()
    return t.replace(' ', '_')

def isLocation(term):
    """
    Check if a given string is a location or not
    location means that the term may be classified in the next resources:
        Place, PopulatedPlace
    term
        string to check if it is a location
    return
        True,  if term is a location
        False, otherwise
    """
    
    # Capitalize each word of the string
    term = normalize(term)

    query = """
        PREFIX res: <http://dbpedia.org/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
	    PREFIX sch: <http://schema.org/>
	    PREFIX umb: <http://umbel.org/umbel/rc/>

        ASK WHERE {
            { res:? rdf:type <http://www.ontologydesignpatterns.org/ont/d0.owl#Location>}
            UNION
            { res:? rdf:type dbo:Location}
            UNION
            { res:? rdf:type dbo:Place}
            UNION
            { res:? rdf:type dbo:PopulatedPlace}
            UNION
            { res:? rdf:type umb:PopulatedPlace}
            UNION
            { res:? rdf:type sch:Place}
            UNION
            { res:? rdf:type sch:Country}
            UNION
            { res:? rdf:type yago:YagoGeoEntity} .
        }
    """

    query = query.replace('?', term)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()

    return result['boolean']

def isCountry(term):
    """
    Check if a given string is a country or not
    term
        string to check if it is a country
    return
        True,  if term is a country
        False, otherwise
    """
    # Capitalize each word of the string
    term = normalize(term)
    
    query = """
        PREFIX res: <http://dbpedia.org/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
	    PREFIX sch: <http://schema.org/>
	    PREFIX umb: <http://umbel.org/umbel/rc/>

        ASK WHERE {
            { res:? rdf:type dbo:Country}
            UNION
            { res:? rdf:type umb:Country}
            UNION
            { res:? rdf:type sch:Country} .
        }
    """

    query = query.replace('?', term)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()

    return result['boolean']

def isCity(term):
    """
    Check if a given string is a city or not
    term
        string to check if it is a city
    return
        True,  if term is a city
        False, otherwise
    """
    
    # Capitalize each word of the string
    term = normalize(term)

    query = """
        PREFIX res: <http://dbpedia.org/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
	    PREFIX sch: <http://schema.org/>
	    PREFIX umb: <http://umbel.org/umbel/rc/>

        ASK WHERE {
            { res:? rdf:type dbo:Settlement}
            UNION
            { res:? rdf:type umb:City}
            UNION
            { res:? rdf:type umb:Village}
            UNION
            { res:? rdf:type sch:City} .
        }
    """

    query = query.replace('?', term)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()

    return result['boolean']

def isRegion(term):
    """
    Check if a given string is a region or not
    term
        string to check if it is a region
    return
        True,  if term is a region
        False, otherwise
    """
    
    # Capitalize each word of the string
    term = normalize(term)

    query = """
        PREFIX res: <http://dbpedia.org/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX sch: <http://schema.org/>

        ASK WHERE {
            { res:? rdf:type dbo:Region}
            UNION
            { res:? rdf:type dbo:AdministrativeRegion}
            UNION
            { res:? rdf:type sch:AdministrativeArea} .
        }
    """

    query = query.replace('?', term)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()

    return result['boolean']
