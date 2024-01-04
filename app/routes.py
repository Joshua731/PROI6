import pandas as pd
import os
from dash_auth import BasicAuth
from sqlalchemy import create_engine
from app import app
from app.templates import interface, pagina_inicial, index, historico_producao, alertas_notificacoes, \
    cadastro_do_usuario, status, editar_status


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


@app.route("/overview")
def redirecionar_home():
    return interface.interface.index()


# @app.route('/cadastro/usuario')
# def cadastrar_usuario():
#     return usuario.cad_usuario.index()


@app.route('/')
def redireciona_inicio():
    return pagina_inicial.inicial.index()


# @app.route('/cadastro/database')
# def redireciona_cadastro():
#     return base_de_dados.cad_banco.index()


# @app.route('/cadastro/colunas/inversores')
# def redirecionar_para_cadastro_dos_inversores():
#     return inversores.inversores.index()


@app.route('/home')
def redirecionar_para_tela_home():
    return index.index.index()


@app.route('/historico_producao')
def redirecionar_para_historico_de_producao():
    return historico_producao.historico_producao.index()


@app.route('/alertas_notificacoes')
def redirecionar_para_alarmes():
    return alertas_notificacoes.alertas_notificacoes.index()


@app.route('/cadastro_usuario')
def redirecionar_para_cadastro_do_usuario():
    return cadastro_do_usuario.cadastro_do_usuario.index()


@app.route('/status')
def redirecionar_status_inversores():
    return status.status.index()

@app.route('/editar_status')
def redirecionar_para_edicao_da_tela_dos_status_dos_inversores():
    return editar_status.edit_status.index()