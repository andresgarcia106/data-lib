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

This library used Keyring so you'll need to create the following Keys in:
    - Windows Password Manager
    - Mac Keychain
    - Linux Secret Service

Required Keys
    - Service:
        - Provider_Environment_User
            - username = "username"
            - password = "database username"
        - Provider_Environment_Password
            - username = "password"
            - password = "database password"
        - Provider_Environment_Host
            - username = "host"
            - password = "host number"
        - Provider_Environment_Port
            - username = "port"
            - password = "port number"
        - Provider_Environment_Database
            - username = "database"
            - password = "database name"

*** Note: **** 
Replace <<Provider>> for your database provider.
Replace <<Environment>> for your database environment (Dev, QA, Stg, Prd etc..)

*** Snowflake SSO: ***

If you will be using Snowflake SSO create your Password Credential with a Blank Password.

```Python
from data_lib import DataGetter

# Instantiate a DB object
db = DataGetter()

# run init_database to connect a Database
db.init_database("<<DB Provider>>", "<<Environment>>")

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


