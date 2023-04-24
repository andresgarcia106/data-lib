# Data Lib
A small library for gathering data and creating reports.

### Installation
Create a new conda environment or virtual env
```cmd

conda create -n <<env_name>> python=3.8 && 
conda activate <<my_env>> && 
conda install pip &&
pip install https://github.com/andresgarcia106/data-lib/releases/latest/download/data-lib.tar.gz

```

### Getting started
Create a config.cfg file, where you place your settings database config and data reporting configs, e.g:

```cfg 

[database]
# type = teradata, oracle, mysql, postgres, mssql, snowflake
# connstring = teradatasql://username:password@host/?database=database
type = {provider}
connstring =  {provider}://{username}:{password}@{host}/?database={database}

[data]
input = /02_data/01_input_files/
queries =  /02_data/02_input_query/
stage = /02_data/03_stage_files/
output =  /02_data/04_output_files/
archived = /02_data/04_archived_files/
report_key =  Key # any string that will help generate a random password for your files

```

You can use more than one db configuration.

Run the following command on your terminal:
```cmd
c-config # to create a config file with the default settings.

```

How to use this lib:

```Python
from data_lib import DataGetter

# Instantiate a DB object
db = DataGetter(db_config, data_config)

# set db engine
engine_one = db.set_engine()

# Set default paths for input, output, query and password tracker folders paths are set based on your root project,
# if folders do not exist will be created automatically
od.set_path()

# Set custom paths for input, queries, staging, output and archive default folders
# Paths you can Set:
- input_data
- query_files
- stage_data
- output_data
- archived_data

od.set_path(set_custom_path=True, path_type="input_data", custom_path="./custom/path")
```
Remember to import your config dictionaries from your config.cfg:

```cfg
config = configparser.RawConfigParser()
config.read('../config.cfg')

db_config = dict(config.items('database'))
data_config = dict(config.items('data'))

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


