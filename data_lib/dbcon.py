from sqlalchemy import create_engine

class DBCon:
    def __init__(self):
        pass

    def set_engine(self, uri):
        """
        It takes a dictionary of connection strings and returns the connection string for the database
        type specified in the config file
        :return: The create_engine function is being returned.
        """

        return create_engine(uri)