# Data Lib
A small library for gathering data and creating reports.

### Installation
Create a new conda environment or virtual env
```cmd

conda create -n <<env_name>> python=3.8 && conda activate <<my_env>> && pip install https://github.com/andresgarcia106/data-lib/releases/latest/download/ag-data-lib.tar.gz

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

Run the following command on your terminal:
```cmd
c-config # to create a config file with the default settings.

```

How to use this lib:

```Python
from data_lib import DB, Data

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

# Create a Project folder

This template includes some basic settings to start working with the library

Run the following command on your terminal:
```cmd
c-project # to create a project folder with a generic name.
or
c-project -n my_project_name # to create a project with a custom name
```

# Create a Jupyter Notebook

This template includes some basic settings to start working with the library

Run the following command on your terminal:
```cmd
c-notebook # to create a notebook with a generic name.
or
c-notebook -n my_notebook_name # to create a notebook with a custom name

```

# Deactivate your conda environment

Run the following command on your terminal:
```cmd
c-deactivate # to deactivate your conda environment

```


