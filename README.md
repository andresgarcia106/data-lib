# AG Data Lib
A small library for gathering data and creating reports.

### Installation
```
pip install https://github.com/jgarciaf106/dataLib/releases/latest/download/ag-data-lib.tar.gz
```

### Getting started
Create a config.py file, where you place your settings database config and data reporting configs, e.g:

```Python 
db_config = {
    "connstring": "mssql+pyodbc://{0}/{1}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server",
    "type": "mssql",
    "server": "db server",
    "database": "db name",
}


data_config = {
    "input": "path",
    "load": "path",
    "output": "path",
    "queries": "path",
    "report_key": "Key", # any string that will help generate a random password for your files
    "font_name": "Arial",
    "header_font_size": 13,
    "header_font_color": 0xFFFFFF,
    "header_bg_color": (0, 150, 214),
    "content_font_size": 12,
}
```

You can use more than one db configuration.


How to use this lib:

```Python
from ag_data_lib import DB, Data

# Instantiate a DB object
db = DB(configs)
od = Data(configs)

# set db engine
engine_one = db.set_engine()

# Set default paths for input, output, query and password tracker folders paths are set based on your root project,
# if folders do not exist will be created automatically
od.set_path()

# Set custom paths for input, output, query and password tracker default folders
# Paths you can Set:
- input_data
- output_data
- query_files
- pass_tracker

od.set_path(set_custom_path=True, path_type="input_data", custom_path="./custom/path")
```
Remember to import your config dictionaries from your config.py like:

```Python 
from config import * 
or
from config import config_one, config_two etc...

```

# Create a Jupyter Notebook

This template includes some basic settings to start working with the library

Run the following command on your terminal:
```cmd
python -m new_notebook # to create a notebook with a generic name.
or
python -m new_notebook -n my_notebook_name # to create a notebook with a custom name

```

# Magic commands

Run the following command on your notebook cell:
```Ipython
%notebook_to_html # to convert the notebook to html.
```