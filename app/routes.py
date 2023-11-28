import pandas as pd
import os
from dash_auth import BasicAuth
from sqlalchemy import create_engine
from app import app
from app.templates import index, interface, pagina_inicial
from app.templates.cadastros import base_de_dados, usuario

engine = create_engine('sqlite:///./database/database.db')

# Create the directory if it does not exist
if not os.path.exists('database'):
    os.makedirs('database')


df = pd.read_sql('SELECT nome_usuario, senha_login FROM usuario', con=engine)
VALID_USERNAME_PASSWORD_PAIRS = {'admin': '123'}
for i in range(len(df)):
    VALID_USERNAME_PASSWORD_PAIRS[f'{df["nome_usuario"].values[i]}'] = f'{df["senha_login"].values[i]}'
    print(VALID_USERNAME_PASSWORD_PAIRS)


# Monkey patch basic auth to work on non-index pages
BasicAuth(pagina_inicial.inicial, VALID_USERNAME_PASSWORD_PAIRS)
# BasicAuth(interface.interface, VALID_USERNAME_PASSWORD_PAIRS)


@app.route("/interface")
def redirecionar_home():
    return interface.interface.index()


@app.route('/cad-usu')
def cadastrar_usuario():
    return usuario.cad_usuario.index()


@app.route('/')
def redireciona_inicio():
    return pagina_inicial.inicial.index()


@app.route('/cad-db')
def redireciona_cadastro():
    return base_de_dados.cad_banco.index()
