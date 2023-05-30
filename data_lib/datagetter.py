# library imports
import os
import json
import platform as pt
import pandas as pd
import xlwings as xw
from xlwings.utils import rgb_to_int
from snowflake.snowpark import Session
from .datalibutils import *
from .dbcon import DBCon 



if pt.system() == "Windows":
   import win32com.client


class DataGetter (DBCon):
    def __init__(self):
        """
        This is the constructor function for a class that sets up various file paths and initializes a
        database engine to None.
        """
        """
        The __init__ function is called when an instance of the class is created.
        :param config: The config object that was created in the previous step
        """
        super().__init__()
        self._root_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self._input_path = self._root_path + "/02_data/01_input_files/"
        self._query_path = self._root_path + "/02_data/02_input_query/"
        self._stage_path = self._root_path + "/02_data/03_stage_files/"
        self._output_path = self._root_path + "/02_data/04_output_files/"      
        self._archived_path = self._root_path + "/02_data/05_archived_files/"
        self._engine =  None

    def init_database(
        
        self, provider, environment
    ):
        """
        This function initializes a database engine with a specified provider and environment.
        
        :param provider: The type of database provider, such as "mysql", "postgresql", "sqlite", etc
        :param environment: The environment parameter is used to specify the environment in which the
        database is being initialized. This could be a development, testing, or production environment,
        for example. The value of this parameter will be used to create the appropriate database URI for
        the specified provider
        """
        db_uri = create_database_uri(provider, environment)
        self._engine = self.set_engine(db_uri)
       
    def snowpark_session(self):
        """
        This function creates a new session for a Snowpark engine using connection parameters.
        :return: a new Snowflake session object created using the connection parameters extracted from
        the SQLAlchemy engine URL.
        """
        
        connection_parameters = self._engine.engine.url.translate_connect_args()
        if len(connection_parameters) == 2:            
            connection_parameters["account"] = connection_parameters.pop("host")
            connection_parameters["user"] = connection_parameters.pop("username")
            connection_parameters["authenticator"] = connection_parameters.pop("username")
        else:
            connection_parameters["user"] = connection_parameters.pop("username")
            connection_parameters["authenticator"] = connection_parameters.pop("username")
            
        new_session = Session.builder.configs(connection_parameters).create()
        return new_session 

    def run_sql_query(self, query, **kwargs):
        """
        This function runs a SQL query and returns the results as a pandas dataframe, with the option to
        pass in parameters using kwargs.
        
        :param query: The SQL query to be executed
        :return: a pandas DataFrame that contains the results of a SQL query.
        """        
       
        out_df = pd.DataFrame()
        query_exists = os.path.exists(self._query_path + f"{query}.sql")
        
        if query_exists:
            if kwargs == {}:
                file_query = open(self._query_path + f"{query}.sql").read()
                out_df = pd.read_sql_query(file_query, self._engine)
            else:
                with open(self._query_path + f"{query}.sql") as get:
                    file_query = get.read()
                out_df = pd.read_sql_query(file_query.format(**kwargs), self._engine)
        else:
            if kwargs == {}:
                out_df = pd.read_sql_query(query, self._engine)
            else:
                out_df = pd.read_sql_query(query.format(**kwargs), self._engine)

        return out_df

    def execute_sql_query(self, query,):
        """
        This function executes a SQL query using a specified engine and query path.
        
        :param query: The SQL query to be executed
        """
        
        self._engine.execute(query) if os.path.exists(
                self._query_path + f"{query}.sql"
            ) else self._engine.execute(query)
        
        self._engine.dispose
        
    def is_connected(self):
        """
        This function checks if a connection to a database is open or not and returns a boolean value
        accordingly.
        :return: a boolean value indicating whether the database connection is currently open or not. If
        the connection is open, it returns True, otherwise it returns False. If an exception occurs
        during the connection attempt, it also returns False.
        """
        try:
            connection = self._engine.connect()
            is_open = connection.closed
            connection.close()
            return not is_open
        except Exception as e:
            return False
        
    def engine(self):
        """
        This function returns the value of the private attribute "engine".
        :return: The method `engine` is being defined as returning the private attribute `__engine` of
        the object.
        """
        return self.__engine
        

    def read_file(self, reader, file_path, **kwargs):
        """
        It takes a function as an argument and returns the result of calling that function on the file
        path

        :param reader: a function that takes a file path and returns a pandas dataframe
        :param file_path: The path to the file to read
        :return: the reader function.
        """
        out_df = (
            reader(self._input_path + file_path, **kwargs)
            if os.path.exists(self._input_path + file_path)
            else reader(file_path, **kwargs)
        )
        return out_df

    def _file_saver(self, data, file_name, protect_file, security_method, auth_users):
        """
        :param data: The data to be written to the Excel file
        :param file_name: The name of the file to be saved
        :param protect_file: If True, the file will be password protected
        :param draft_email: If True, the email will be saved as a draft. If False, the email will be
        sent immediately
        :param requester: The email address of the requester
        :param email_folder: The folder where the email will be saved
        """

        # Before saving the file set DisplayAlerts to False to suppress the warning dialog:

        # remove existing files before save
        file_cleaner(f"{self._output_path}{file_name}")

        # default password
        file_password = None
        # file_format = file_format_constant(file_name)

        output_path = f"{self._output_path}{file_name}"

        # workbook / sheet variables
        app = xw.App(visible=False)
        wb = xw.Book()
        ws = wb.sheets[0]
        ws.name = "Data Export"

        # excel data 
        ws.range("A1").options(pd.DataFrame, index=False).value = number_to_string(data)

        # save password protect file if needed
        try:
            if protect_file:
                if security_method == "PWD":
                    file_password = password_generator("PWD")
                    wb.save(output_path)
                    wb.close()
                    app.quit()

                    # password protect file
                    excel = win32com.client.gencache.EnsureDispatch("Excel.Application")
                    excel.DisplayAlerts = False
                    book = excel.Workbooks.Open(output_path)
                    book.SaveAs(output_path, 51, file_password)
                    book.Close()
                    excel.Application.Quit()

                    # update password tracker
                    self._password_tracker(
                        self._today,
                        file_name,
                        file_password,
                    )

                if security_method == "RMS":
                    active_book = xw.books.active
                    for auth_user in auth_users:
                        active_book.api.Permission.Add(auth_user, 15)
                    wb.save(output_path)
                    wb.close()
                    app.quit()
            else:
                wb.save(output_path)
                wb.close()
                app.quit()

        except Exception as e:
            raise

    def export_data(
        self,
        odf,
        custom_filename=None,
        protect_file=False,
        security_method=None,
        auth_users=[],
    ):
        # assign file name
        file_name = file_namer(custom_filename)

        # save file
        self._file_saver(odf, file_name, protect_file, security_method, auth_users)
