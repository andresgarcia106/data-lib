
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
            "postgres": self._cfg["connstring"].format(
                self._cfg["user"],
                self._cfg["password"],
                self._cfg["server"],
                self._cfg["database"],
            ),
            "mssql": self._cfg["connstring"].format(
                self._cfg["server"], self._cfg["database"]
            ),
            "oracle": self._cfg["connstring"].format(
                self._cfg["user"],
                self._cfg["password"],
                self._cfg["server"],
                self._cfg["database"],
            ),
            "mysql": self._cfg["connstring"].format(
                self._cfg["user"],
                self._cfg["password"],
                self._cfg["server"],
                self._cfg["database"],
            ),
            "sqlite": self._cfg["connstring"].format(
                self._cfg["user"],
                self._cfg["password"],
                self._cfg["server"],
                self._cfg["database"],
            ),
            "teradata": self._cfg["connstring"].format(
                self._cfg["user"],
                self._cfg["password"],
                self._cfg["server"],
                self._cfg["database"],
            ),
        }

        return create_engine(engines.get(self._cfg["type"]))