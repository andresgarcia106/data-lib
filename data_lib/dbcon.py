from sqlalchemy import create_engine
from snowflake.snowpark import Session

class DBCon:
    def __init__(self):
        pass

    def set_engine(self, uri):
        """
        It takes a dictionary of connection strings and returns the connection string for the database
        type specified in the config file
        :return: The create_engine function is being returned.
        """
        engine = None
        
        if isinstance(uri, dict):
            engine = Session.builder.configs(uri).create()
        else:
            engine = create_engine(uri)
        
        return engine
    
    def create_sf_session(self, uri):
        """
        Creates a Snowflake session
        """
        session = None
        session = Session.builder.configs(self._uri).create()
        return session