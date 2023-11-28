import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///./database/database.db')

df = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con=engine)
print(df)

df = pd.read_sql('SELECT * FROM usuario;', con=engine)
print(df)

df = pd.read_sql('SELECT * FROM database;', con=engine)
print(df)
