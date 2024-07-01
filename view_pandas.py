import pandas as pd
import pyodbc
host='localhost'
port=31010
uid ='admin'
pwd = 'admin123'
driver = '/opt/arrow-flight-sql-odbc-driver/lib64/ libarrow-odbc.so.0.9.1.168'
cnxn = pyodbc.connect("Driver={};ConnectionType=Direct;HOST={};PORT={};AuthenticationType=Plain;UID={};PWD={}".format(driver,host,port,uid,pwd),autocommit=True)
sql = "SELECT * FROM \"DBT Semantic Layer.Data Science.sp500_stock\""
df = pd.read_sql(sql,cnxn)