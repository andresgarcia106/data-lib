# library imports
from dbcon import DBCon 
import os
import json
import win32com.client
import pandas as pd
import xlwings as xw
from xlwings.utils import rgb_to_int
from .utils import *
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine


class DataGetter (DBCon):
    def __init__(self, db_cfg, data_cfg):
        """
        The __init__ function is called when an instance of the class is created.
        :param config: The config object that was created in the previous step
        """
        super().__init__(db_cfg)
        self._cfg = data_cfg
        self._root_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self._output_path = None
        self._query_path = None
        self._input_path = None
        self._pass_path = None

    def set_path(
        self,
        set_cfg_paths=True,
        set_custom_path=False,
        path_type=None,
        custom_path=None,
    ):
        """
        :param set_custom_path: If you want to set a custom path, set this to True, defaults to False
        (optional)
        :param path_type: The type of path you want to set
        :param custom_path: the path to the folder where the files are located
        """
        if set_cfg_paths:
            self._input_path = self._root_path + self._cfg["input"]
            self._output_path = self._root_path + self._cfg["output"]
            self._query_path = self._root_path + self._cfg["queries"]
            self._pass_path = self._root_path + self._cfg["tracker"]
        else:
            if set_custom_path:
                if path_type == "output_data":
                    self._output_path = custom_path
                elif path_type == "query_files":
                    self._query_path = custom_path
                elif path_type == "input_data":
                    self._input_path = custom_path
                elif path_type == "pass_tracker":
                    self._pass_path = custom_path
            else:
                paths = create_path()
                (
                    self._input_path,
                    self._output_path,
                    self._query_path,
                    self._pass_path,
                ) = paths

    def run_sql_query(self, query, **kwargs):
        """
        If the query is a file, then read the file and pass it to the database engine. If the query is a
        string, then pass the string to the database engine

        :param query: The name of the query file to be run
        :param db_engine: the database engine
        :return: A dataframe
        """
        db_engine = self.set_engine()
        
        out_df = pd.DataFrame()

        if os.path.exists(self._query_path + f"{query}.sql"):
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

    def execute_sql_query(self, query):
        """
        Execute a query file or inline query using the engine

        :param query: The name or file name of the sql script to execute
        """
        db_engine = self.set_engine()
        
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

        # excel data header formatting
        ws.range("A1").options(pd.DataFrame, index=False).value = number_to_string(data)
        header_format = ws.range("A1").expand("right")
        header_format.color = rgb_to_int(eval(self._cfg["header_bg_color"]))
        header_format.api.Font.Name = self._cfg["font_name"]
        header_format.font.color = rgb_to_int(eval(self._cfg["header_font_color"]))
        header_format.api.Font.Bold = True
        header_format.api.Font.Size = self._cfg["header_font_size"]

        # excel data content formatting
        data_format = ws.range("A2").current_region
        data_format.api.Font.Name = self._cfg["font_name"]
        data_format.api.Font.Size = eval(self._cfg["content_font_size"])

        # save password protect file if needed
        try:
            if protect_file:
                if security_method == "PWD":
                    file_password = password_generator(self._cfg["report_key"])
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
