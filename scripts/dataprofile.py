from base64 import encode
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
from os import listdir
import sys, os
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv

# env
project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(project_folder, ".env"))

# from env
# SQL conn data
cnnhost = os.getenv("SQL_HOST")
cnnport = os.getenv("SQL_PORT")
cnndb = os.getenv("SQL_DBSTAGE")
cnnuser = os.getenv("SQL_USER")
cnnpwd = os.getenv("SQL_PWD")

engine = create_engine(
    "mssql+pyodbc://"
    f"{cnnuser}:{cnnpwd}@{cnnhost}:{cnnport}/{cnndb}?"
    "driver=" + os.getenv("SQL_ODBC_DRIVER")
)
conn = engine.connect()

# fn
def fExtract(data, dataprofiles, dataprofiles_prefix):
    name = data["name"]
    print("-->", name)
    df = pd.read_sql("SELECT * from " + name, engine)
    print(df)
    profile = ProfileReport(df, title=f"{name} Profiling Report", minimal=True)
    profile.to_file(f"{dataprofiles}{dataprofiles_prefix}_{name}.html")

# function that uses fExtract to create profiles based on the data objects in the database
# inputs: 
# - type (table or view), 
# - prefix (prefix of the data objects to be profiled)
# - dataprofiles_prefix (prefix for the profile file names
def create_profiles(type,dataobject_prefix, file_prefix):

    if type == 'tables':
        sql_tables = """
        SELECT t.name AS name 
        FROM sys.schemas AS s 
        JOIN sys.tables AS t ON t.schema_id = s.schema_id 
        WHERE 
        t.name like '{dataobject_prefix}%' 
        ORDER BY 1
        """.format(dataobject_prefix=dataobject_prefix)

        # get list for tables
        tables = conn.execute(sql_tables)
        print("--> extracting views..")

        # TABLES per row
        for table in tables:
            fExtract(table, dataprofiles, file_prefix + "_Tbl_")

    if type == 'views':
        # get list for views

        # specific 
        sql_views = """
        SELECT v.name as name FROM sys.views as v where v.name like '{dataobject_prefix}%' ORDER BY 1;
        """.format(dataobject_prefix=dataobject_prefix)

        # get list for tables
        views = conn.execute(sql_views)
        print("--> extracting tables..")

        # VIEWS per row
        for view in views:
            fExtract(view, dataprofiles, file_prefix + "_Vws_")

# define params:
dataprofiles = "data-profiles/" # folder to save the profiles
# params
type = 'tables' # 'tables' or 'views
dataobject_prefix = 'stg_nv' # prefix of the data objects to be profiled
file_prefix = 'rd' # prefix for the profile file names

# run
create_profiles(type,dataobject_prefix,file_prefix)
