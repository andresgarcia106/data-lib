from sqlalchemy import create_engine


class DBCon:
        
    def __init__(self):
        self._engine_args = None
        pass

    def set_engine(self, uri):
        """
        It takes a dictionary of connection strings and returns the connection string for the database
        type specified in the config file
        :return: The create_engine function is being returned.
        """
        engine = create_engine(uri)   
        self.engine_args(engine)  
        return engine 
    
    def engine_args(self, db_engine):
        """
        This function takes a database engine and extracts connection parameters to be used as arguments
        for another function.
        
        :param db_engine: It is a parameter that represents a database engine object. The function is
        using this object to extract connection parameters such as host, username, and authentication
        method
        """
        connection_parameters = db_engine.engine.url.translate_connect_args()
        if len(connection_parameters) == 2:            
            connection_parameters["account"] = connection_parameters.pop("host")
            connection_parameters["user"] = connection_parameters.pop("username")
            connection_parameters["authenticator"] = "externalbrowser"
        else:
            connection_parameters["user"] = connection_parameters.pop("username")
            connection_parameters["authenticator"] = connection_parameters.pop("username")
        self._engine_args = connection_parameters
        