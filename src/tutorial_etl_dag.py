import time
from datetime import datetime
from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.providers.miecrosoftmssqlhooks.mssql import MsSqlHook
from airflow.hooks.base_hook import BaseHook
import pandas as pd
from sqlalchemy import create_engine

@task()

#get from db
def get_src_tables():
    hook = MsSqlHook(mssql_conn_id = "sqlserver")
    sql = """"""
    df = hook.get_pandas_df(sql)
    print(df)
    tbl_dict = df.to_dict('dict')
    return tbl_dict

# transfer to another db
@task()
def load_src_data(tbl_dict: dict):
    conn = BaseHook.get_connection("postgres")
    engine = create_engine(f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}")
    all_tbl_name = []
    start_time = time.time()
    
    #Access the table_name element in dictionaries
    
    for key, val in tbl_dict["table_name"].items():
        all_tbl_name.append(val)
        rows_imported = 0
        sql = f"select * from {val}"
        hook = MsSqlHook(mssql_conn_id = "sqlserver")
        df = hook.get_pandas_df(sql)
        print(f"Importing rows {rows_imported} to {rows_imported + len(df)} for table {val}")
        df.to_sql(f'src_{val}', engine, if_exists="replace", index = False)
        rows_imported += len(df)
        print(f"Completed. {str(round(time.time() - start_time, 2))} seconds elapsed")
    print("Data imported sucessfully")
    return all_tbl_name

#data transformation if needed
@task()
def transform_srcProduct():
    conn = BaseHook.get_connection("postgres")
    engine = create_engine(f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}")
    pdf = pd.read_sql_query("SELECT * FROM bla bla bla")
    
    #drop columns not needed
    #subset those columns that are needed
    revised = pdf[["ProductKey", "ProductAlternateKey", "bla bla bla"]]
    #replace nulls using fillna example here:
    revised["WeightUnitMeasureCode"].fillna("0", inplace = True)
    
    #Renaming columns if needed
    revised = revised.rename(columns = {"EnglishDescription" : "Description"})
    
    #return back to sql
    revised.to_sql()
