# -*- coding: utf-8 -*-

class Query:
    """ A useful class to manage the differents querie. 
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

    
    def set_queryno(self,queryno):
        """ Setter of the variable queryno.
        
        Keyword arguments:
        self -- the pointer to this class
        local -- the value for variable queryno
        
        """
        self._queryno = queryno
    
    def get_queryno(self):
        """ Getter of the variable queryno.
        
        Return:
        The value of the variable queryno: str      
        """
        return self._queryno
    
    def set_query(self,query):
        """ Setter of the variable query.
        
        Keyword arguments:
        self -- the pointer to this class
        local -- the value for variable query
        
        """
        self._query = query
    
    def get_query(self):
        """ Getter of the variable query.
        
        Return:
        The value of the variable query: str or None      
        """
        return self._query
        
    def set_local(self,local):
        """ Setter of the variable local.
        
        Keyword arguments:
        self -- the pointer to this class
        local -- the value for variable local
        
        """
        self._local = local
    
    def get_local(self):
        """ Getter of the variable local.
        
        Return:
        The value of the variable local: str or None      
        """
        return self._local
    
    def isLocal():
        """ Know if this variable is a localization or not.
        
        Return:
        0 -- the query is not local
        1 -- the query is local
        
        """
        return str(self._local).upper()=='YES'
    
    def set_what(self,what):
        """ Setter of the variable what.
        
        Keyword arguments:
        self -- the pointer to this class
        what -- the value for variable what
        
        """
        self._what = what
        
    def get_what(self):
        """ Getter of the variable what.
        
        Return:
        The value of the variable what: str or None      
        """
        return self._what        
    
    def set_whattype(self,whatType):
        """ Setter of the variable whatType.
        
        Keyword arguments:
        self -- the pointer to this class
        local -- the value for variable whatType
        
        """
        self._whatType = whatType
    
    def get_whattype(self):
        """ Getter of the variable whatType.
        
        Return:
        The value of the variable whatType: str or None      
        """
        return self._whatType
    
    def set_georelation(self,geoRelation):
        """ Setter of the variable geoRelation.
        
        Keyword arguments:
        self -- the pointer to this class
        local -- the value for variable geoRelation
        
        """
        self._geoRelation = geoRelation
    
    def get_georelation(self):
        """ Getter of the variable geoRelation.
        
        Return:
        The value of the variable geoRelation: str or None      
        """
        return self._geoRelation 

    def set_where(self,where):
        """ Setter of the variable where.
        
        Keyword arguments:
        self -- the pointer to this class
        local -- the value for variable where
        
        """
        self._where = where
    
    def get_where(self):
        """ Getter of the variable where.
        
        Return:
        The value of the variable where: str or None      
        """
        return self._where
    
    def set_latlong(self,latLong):
        """ Setter of the variable latLong.
        
        Keyword arguments:
        self -- the pointer to this class
        local -- the value for variable latLong
        
        """
        self._latLong = latLong
    
    def get_latlong(self):
        """ Getter of the variable latLong.
        
        Return:
        The value of the variable latLong: str or None      
        """
        return self._latLong    
    
    def __str__(self):
        return 'QUERY '+str(self._queryno)+": "+str(self._query)+"\n\t LOCAL: "+str(self._local)+"\n\t WHAT: "+str(self._what)+"\n\t WHAT-TYPE: "+str(self._whatType)+"\n\t GEO-RELATION: "+str(self._geoRelation)+"\n\t WHERE: "+str(self._where)+"\n\t LAT-LONG: "+str(self._latLong)
