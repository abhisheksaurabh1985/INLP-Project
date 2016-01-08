class Query:
    """ A useful class to manage the differents queries. 
    A query is formed by a id (queryno) and other attributes
    like the query."""
    
    def __init__(self, queryno):
        """ Constructor of Query class.
        
        Keyword argument:
        queryno -- the id number
        
        """
        self._queryno = queryno
        self._query = None
        self._local = None
        self._what = None
        self._whatType = None
        self._geoRelation = None
        self._where = None
        self._latLong = None
    
    def __str__(self):
        return 'QUERY '+str(self._queryno)+": "+str(self._query)+"\n\t LOCAL: "+str(self._local)+"\n\t WHAT: "+str(self._what)+"\n\t WHAT-TYPE: "+str(self._whatType)+"\n\t GEO-RELATION: "+str(self._geoRelation)+"\n\t WHERE: "+str(self._where)+"\n\t LAT-LONG: "+str(self._latLong)

