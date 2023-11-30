import pandas as pd
from sqlalchemy import create_engine

# Carregar o arquivo CSV para um DataFrame
file_path = 'app/files/saida_atualizado.csv'
data = pd.read_csv(file_path)

# Configurações de conexão com o banco de dados
# Substitua 'seu_banco_de_dados' e outras informações de acordo com o seu banco

# Construir a string de conexão com o banco de dados usando SQLAlchemy
connection_str = 'sqlite:///./database/database.db'
engine = create_engine(connection_str)

# Carregar os dados do DataFrame para o banco de dados como uma nova tabela
table_name = 'cidades'  # Nome da tabela que será criada no banco de dados

data.to_sql(table_name, engine, index=False, if_exists='replace')
# O parâmetro if_exists='replace' irá substituir a tabela se ela já existir, use 'append' se quiser adicionar a uma tabela existente
