# library imports
import os
import json
import platform as pt
import pandas as pd
import xlwings as xw
from xlwings.utils import rgb_to_int
from .datalibutils import *
from .dbcon import DBCon 


if pt.system() == "Windows":
   import win32com.client


class DataGetter (DBCon):
    def __init__(self):
        """
        The __init__ function is called when an instance of the class is created.
        :param config: The config object that was created in the previous step
        """
        super().__init__()
        self._root_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self._uri = None
        self._input_path = None
        self._query_path = None
        self._stage_path = None
        self._output_path = None      
        self._archived_path = None
        self._sf_session = None

    def set_config(
        self, provider
    ):
        """
        :param set_custom_path: If you want to set a custom path, set this to True, defaults to False
        (optional)
        :param path_type: The type of path you want to set
        :param custom_path: the path to the folder where the files are located
        """
        
        self._uri = create_database_uri(provider)
        self._input_path = self._root_path + "/02_data/01_input_files/"
        self._query_path = self._root_path + "/02_data/02_input_query/"
        self._stage_path = self._root_path + "/02_data/03_stage_files/"
        self._output_path = self._root_path + "/02_data/04_output_files/"
        self._archived_path = self._root_path + "/02_data/05_archived_files/"
        
    def set_session(self):
        self._sf_session = self.create_sf_session(self._uri)

    def run_sql_query(self, query, snowflake = False, **kwargs):
        """
        If the query is a file, then read the file and pass it to the database engine. If the query is a
        string, then pass the string to the database engine

        :param query: The name of the query file to be run
        :param db_engine: the database engine
        :return: A dataframe
        """
        db_engine = self.set_engine(self._uri)
        out_df = pd.DataFrame()
        query_exists = os.path.exists(self._query_path + f"{query}.sql")
        
        if snowflake:
            if query_exists:
                if kwargs == {}:
                    file_query = open(self._query_path + f"{query}.sql").read()
                    out_df = self._sf_session.sql(file_query).to_pandas()
                else:
                    with open(self._query_path + f"{query}.sql") as get:
                        file_query = get.read()
                    out_df = self._sf_session.sql(file_query.format(**kwargs)).to_pandas()
            else:
                if kwargs == {}:
                    out_df = self._sf_session.sql(file_query).to_pandas()
                else:
                    out_df = self._sf_session.sql(file_query.format(**kwargs)).to_pandas()
            self._sf_session.close()
        else:
            if query_exists:
                if kwargs == {}:
                    file_query = open(self._query_path + f"{query}.sql").read()
                    out_df = pd.read_sql_query(file_query, db_engine)
                else:
                    with open(self._query_path + f"{query}.sql") as get:
                        file_query = get.read()
                    out_df = pd.read_sql_query(file_query.format(**kwargs), db_engine)
            else:
                if kwargs == {}:
                    out_df = pd.read_sql_query(query, db_engine)
                else:
                    out_df = pd.read_sql_query(query.format(**kwargs), db_engine)

        return out_df

    def execute_sql_query(self, query, snowflake=False):
        """
        Execute a query file or inline query using the engine

        :param query: The name or file name of the sql script to execute
        """
        db_engine = self.set_engine(self._uri)
        
        if snowflake:
            self._sf_session.sql(query).collect() if os.path.exists(
                self._query_path + f"{query}.sql"
                 ) else self._sf_session.sql(query).collect()
            self._sf_session.close()
        else:
            db_engine.execute(query) if os.path.exists(
                self._query_path + f"{query}.sql"
            ) else db_engine.execute(query)

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
