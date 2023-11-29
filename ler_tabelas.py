import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///./database/database.db')
engine_sql_server = create_engine(f'mssql+pyodbc://capua:Capua123#@201.48.100.251:1434/bancobrasil?driver=ODBC+Driver+17+for+SQL+Server')


df = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con=engine)
print(df)

df = pd.read_sql('SELECT * FROM usuario;', con=engine)
print(df)

df = pd.read_sql('SELECT * FROM database;', con=engine)
print(df)

df = pd.read_sql('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS', con=engine_sql_server)
print(df['TABLE_NAME'].unique())

df = pd.read_sql('SELECT * FROM colunas_database', con=engine)
print(df)
