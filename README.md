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

How to use this lib:

```Python
from data_lib import DataGetter

# Instantiate a DB object
db = DataGetter("<<DB Provider>>")

```

## DB Provider Options 
```
"mssql": "MSSQL",
"mysql": "MySQL",
"teradata": "Teradata",
"postgresql": "PostgreSQL",
"sqlite": "SQLite",
"snowflake": "Snowflake"
```

# set db configuration
```Python
db.set_config()

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


