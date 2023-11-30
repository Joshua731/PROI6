from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.models.bancos import Bancos

# Criar um engine para o banco de dados SQLite
engine = create_engine('sqlite:///./database/database.db', echo=True)  # Substitua pelo nome do seu banco de dados

# Query de criação da tabela em formato de string
q_usuario = """CREATE TABLE IF NOT EXISTS usuario (id_login INTEGER PRIMARY KEY AUTOINCREMENT, nome_usuario TEXT, nome_empresa TEXT, email_login TEXT, senha_login TEXT, data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP);"""
q_db = """CREATE TABLE IF NOT EXISTS database (id_db INTEGER PRIMARY KEY, tipo_banco TEXT, base_de_dados TEXT, usuario_db TEXT, senha_db TEXT, ip TEXT, porta INTEGER, data_insercao DATETIME DEFAULT CURRENT_TIMESTAMP, usuario_id INTEGER REFERENCES usuario(id_login));"""

q_del = """DROP TABLE IF EXISTS usuario_sistema;"""

q_del_row = "DELETE FROM usuario"

q_bancos = """
CREATE TABLE bancos (
    id_banco INTEGER PRIMARY KEY,
    tipo TEXT,
    base TEXT,
    user TEXT,
    pwd TEXT,
    ip TEXT,
    port INTEGER,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

q_update = """
UPDATE cidades
SET value = 1
WHERE name = 'Cachoeira Paulista';
"""

Session = sessionmaker(bind=engine)
session = Session()
session.execute(text(q_update))
# session.execute(text(q_qtdd))
# session.execute(text(q_cd))
# session.execute(text(q_usuario))
# session.execute(text(q_db))
# session.execute(text(q_del))
# session.execute(text(q_del_row))
# session.execute(text(q_bancos))
# Commit para confirmar as alterações no banco de dados
session.commit()

# novo_banco = Bancos(
#     tipo='SQL Server',
#     base='UFV_Suzano',
#     user='administrador',
#     pwd='20ca11ad20!!',
#     ip='40.114.35.162',
#     port=1433,
# )
# session.add(novo_banco)
# session.commit()
# Fechar a sessão
session.close()
