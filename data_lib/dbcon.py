from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

class DBCon:
    def __init__(self, db_cfg):
        self._cfg = db_cfg

    def set_engine(self):
        """
        It takes a dictionary of connection strings and returns the connection string for the database
        type specified in the config file
        :return: The create_engine function is being returned.
        """

        engines = {
            "postgres": self._cfg["connstring"],
            "mssql": self._cfg["connstring"],
            "oracle": self._cfg["connstring"],
            "mysql": self._cfg["connstring"],
            "sqlite": self._cfg["connstring"],
            "teradata": self._cfg["connstring"],            
            "snowflake": self._cfg["connstring"],
        }

        return create_engine(engines.get(self._cfg["type"]))