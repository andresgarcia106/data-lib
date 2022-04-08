# Data Lib
A small library for gathering data and creating reports.

### Installation
```
pip install ag-data-lib
```

### Get started
Create a config.py file, where you place all of your settings, e.g:

```Python 
db_config = {
    "connstring": "mssql+pyodbc://{0}/{1}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server",
    "type": "mssql",
    "server": "db server",
    "database": "db name",
}

dir_paths = {
    "input": path ,
    "load": path ,
    "output": path ,
    "queries": path ,
}
```

You can use more than one db configuration.


How to use this lib:

```Python
from data_lib import DB, Data

# Instantiate a DB object
db = DB(configs)
od = Data(configs)

# set db engine
engine_one = db.set_engine()

# Set paths for input, output folders
od.set_path()
```
Remember to import your config dictionaries from your config.py like:

```Python 
from config import * 
or
from config import config_one, config_two etc...

```