import keyring as kr, datetime as dt, nbformat as nbf, os
from nbconvert.exporters import HTMLExporter
from nbconvert.preprocessors import TagRemovePreprocessor
from traitlets.config import Config
from snowflake.sqlalchemy import URL


# delete existing file
def file_cleaner(file_name):
    """
    Deletes any old file before storing an updated file

    Parameters
    ----------
    file_name : str
        The file location and name to be deleted
    """

    if os.path.exists(file_name):
        os.remove(file_name)


# trims whitespaces
def column_trim(df):
    """
    Trims any trailing spaces on string dataframe columns

    Parameters
    ----------
    df : dataframe
        The dataframe that needs column trims

    Returns
    -------
    dataframe
        a dataframe with all column strings trimmed
    """

    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def file_format_constant(file_name):
    """
    Returns the file format constant
    """
    extension = file_name.split(".")[-1]
    constant = 0

    if extension == "xlsb":
        constant = 50
    elif extension == "xlsx":
        constant = 51
    elif extension == "xlsm":
        constant = 52
    elif extension == "csv":
        constant = 62

    return constant


def number_to_string(df):
    """
    Converts a column of numbers to strings

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to be converted
    column_name : str
        The column name to be converted

    Returns
    -------
    pandas.DataFrame
        The converted dataframe
    """
    for col in df.columns:
        if "ID" in col:
            df[col] = "'" + df[col]
            return df
        else:
            return df


def password_generator(co_key):
    """
    It takes a string as an argument and returns a string that is the concatenation of the argument and
    the current time

    :param co_key: This is the company key that is used to identify the company
    :return: the concatenation of the co_key and the current time.
    """
    return co_key + str(dt.datetime.today().strftime("%I%M%S"))


def file_namer(file_name):
    # assign file name
    if file_name is None:
        file_name = "Report " + dt.datetime.today().strftime("%Y-%m-%d") + ".xlsb"
    else:
        file_name = file_name

    return file_name


def notebook_to_html(notebook_path, html_path):
    """
    It takes a Jupyter notebook and converts it to an HTML file

    :param notebook_path: The path to the notebook you want to convert
    :param html_path: The path to the output HTML file
    """
    # Setup config
    cfg = Config()

    cfg.TemplateExporter.exclude_input = True
    cfg.TemplateExporter.exclude_input_prompt = True
    cfg.TagRemovePreprocessor.enabled = True

    # Configure and run out exporter
    cfg.HTMLExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

    exporter = HTMLExporter(config=cfg)
    exporter.register_preprocessor(TagRemovePreprocessor(config=cfg), True)

    # Configure and run our exporter - returns a tuple - first element with html,
    # second with notebook metadata
    try:
        output = HTMLExporter(config=cfg).from_filename(notebook_path)
        html_output_name = notebook_path.rsplit(".", 1)[0] + ".html"
        # Write to output html file
        with open(html_path + f"/{html_output_name}", "w", encoding="utf8") as f:
            f.write(output[0])
    except FileNotFoundError:
        print("Notebook not found. Review the Notebook path.")


def create_folder_tree(root_folder, sub_dir_folder, folder_list, path):
    # Create directory
    try:
        # Create target Directory
        os.mkdir(path + root_folder)
        os.mkdir(path + root_folder + "/" + sub_dir_folder)
        print(f"Directory {root_folder} and {sub_dir_folder} created")
    except FileExistsError:
        os.mkdir(path + root_folder + "/" + sub_dir_folder)
        print("Directory ", root_folder, " already exists")

    for folder in folder_list:
        try:
            # Create target Directory
            os.mkdir(path + root_folder + "/" + sub_dir_folder + "/" + folder)
            print(f"Directory {folder} created")
        except FileExistsError:
            print("Directory ", folder, " already exists")


def get_database_credentials(input_provider):
    """
    Retrieves the database credentials for the given provider and database name from the kr.
    """
    # Map the provider names to the corresponding kr service names
    kr_services = {
        "mssql": "MSSQL",
        "mysql": "MySQL",
        "teradata": "Teradata",
        "postgresql": "PostgreSQL",
        "sqlite": "SQLite",
        "snowflake": "Snowflake",
        "snowflakeSSO": "Snowflake",
    }
    
    # convert input provider to lower match casing
    provider = input_provider.lower()
    
    # Validate the provider name
    if provider not in kr_services:
        raise ValueError(
            f"Unsupported provider: {provider}. Supported providers: {', '.join(kr_services.keys())}"
        )

    # Get the database credentials from the kr
    try:
        username = kr.get_password(kr_services[provider] + "_U", f"{provider}_username")
        password = kr.get_password(kr_services[provider] + "_P", f"{provider}_password")
        host = kr.get_password(kr_services[provider] + "_H", f"{provider}_host")
        port = kr.get_password(kr_services[provider] + "_A", f"{provider}_port")
        database = kr.get_password(kr_services[provider] + "_D", f"{provider}_database")
    except kr.errors.NokrError:
        print(f"No kr service available for provider: {provider}.")
        print(
            f"To use this function, you must store the database credentials for the {provider} provider in the kr."
        )
        print(
            f"Use the following key names in the kr: {provider}_username, {provider}_password, {provider}_host, {provider}_port, {provider}_database (if applicable)"
        )
        return None
    except kr.errors.PasswordSetError:
        print(
            f"Error retrieving database credentials from kr for provider: {provider}."
        )
        print(
            f"Make sure the database credentials are stored in the kr using the following key names: {provider}_username, {provider}_password, {provider}_host, {provider}_port, {database_name}_database (if applicable)"
        )
        return None

    # Validate the database credentials
    if not all([username, password, host, port, database]):
        print(
            f"Missing or incomplete database credentials for provider: {provider}"
        )
        print(
            f"Make sure the following keys are set in the system keyring service: {provider}_username, {provider}_password, {provider}_host, {provider}_port, {provider}_database (if applicable)"
        )
        return None

    return username, password, host, port, database


def create_database_uri(provider, schema=None, warehouse=None):
    """Generates a database URI for the given provider using the credentials stored in the keyring.
    Supported providers: mssql, mysql, teradata, postgresql, sqlite, snowflake, amazon, azure.
    """

    # Get the database credentials from the keyring
    credentials = get_database_credentials(provider)
    # # Generate the database URI
    if provider == "mssql":
        db_uri = f"mssql+pyodbc://{credentials[0]}:{credentials[1]}@{credentials[2]}:{credentials[3]}/{credentials[4]}?driver=ODBC+Driver+17+for+SQL+Server"
    elif provider == "mysql":
        db_uri = f"mysql+pymysql://{credentials[0]}:{credentials[1]}@{credentials[2]}:{credentials[3]}/{credentials[4]}"
        if schema:
            db_uri += f"?charset=utf8mb4&local_infile=1&autocommit=true&cursorclass=pymysql.cursors.DictCursor&database={schema}"
    elif provider == "teradata":
        db_uri = f"teradatasql://{credentials[0]}:{credentials[1]}@{credentials[2]}/?DATABASE={credentials[4]}"
    elif provider == "postgresql":
        db_uri = f"postgresql://{credentials[0]}:{credentials[1]}@{credentials[2]}:{credentials[3]}/{credentials[4]}"
    elif provider == "sqlite":
        db_uri = f"sqlite:///{credentials[4]}"
    elif provider == "snowflake":
        db_uri = f"snowflake://{credentials[0]}:{credentials[1]}@{credentials[2]}/{credentials[4]}?warehouse={warehouse}&role=SYSADMIN&schema={schema}&authenticator=externalbrowser"
    elif provider == "snowflakeSSO":
        db_uri = URL(
                    account = credentials[2],
                    user = credentials[0],
                    authenticator = 'externalbrowser'
                )
    else:
        raise ValueError(
            f"Unsupported provider: {provider}. Supported providers: mssql, mysql, teradata, postgresql, sqlite, snowflake."
        )

    return db_uri
