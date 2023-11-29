from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Criar um engine para o banco de dados SQLite
engine = create_engine('sqlite:///./database/database.db', echo=True)  # Substitua pelo nome do seu banco de dados

# Query de criação da tabela em formato de string
q_usuario = """CREATE TABLE IF NOT EXISTS usuario (id_login INTEGER PRIMARY KEY AUTOINCREMENT, nome_usuario TEXT, nome_empresa TEXT, email_login TEXT, senha_login TEXT, data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP);"""
q_db = """CREATE TABLE IF NOT EXISTS database (id_db INTEGER PRIMARY KEY, tipo_banco TEXT, base_de_dados TEXT, usuario_db TEXT, senha_db TEXT, ip TEXT, porta INTEGER, data_insercao DATETIME DEFAULT CURRENT_TIMESTAMP, usuario_id INTEGER REFERENCES usuario(id_login));"""

q_del = """DROP TABLE IF EXISTS usuario_sistema;"""

q_del_row = "DELETE FROM database"
Session = sessionmaker(bind=engine)
session = Session()

# session.execute(text(q_qtdd))
# session.execute(text(q_cd))
# session.execute(text(q_usuario))
# session.execute(text(q_db))
# session.execute(text(q_del))
# session.execute(text(q_del_row))
# Commit para confirmar as alterações no banco de dados
session.commit()

# Fechar a sessão
session.close()
