import dash_auth
import pandas as pd
from dash_auth import BasicAuth
from flask import request
from sqlalchemy import create_engine

from app import app
from app.configs import db
from app.models.usuario_sistema import UsuarioSistema
from app.templates import index, interface, pagina_inicial
from app.templates.usuario import cadastro

string_conexao = f'mysql+mysqlconnector://root:Joshua10!@localhost/dashua'

# Cria a engine usando o create_engine do SQLAlchemy
engine = create_engine(string_conexao)

df = pd.read_sql('SELECT nome_usuario, senha_login FROM usuario_sistema', con=engine)
VALID_USERNAME_PASSWORD_PAIRS = {}
for i in range(len(df)):
    VALID_USERNAME_PASSWORD_PAIRS[f'{df["nome_usuario"].values[i]}'] = f'{df["senha_login"].values[i]}'
    print(VALID_USERNAME_PASSWORD_PAIRS)


# Monkey patch basic auth to work on non-index pages
def basic_auth_wrapper(basic_auth, func):
    """Updated auth wrapper to work on all pages rather than just index"""

    def wrap(*args, **kwargs):
        if basic_auth.is_authorized():
            return func(*args, **kwargs)
        return basic_auth.login_request()

    return wrap


BasicAuth.auth_wrapper = basic_auth_wrapper

auth_home = BasicAuth(index.index, VALID_USERNAME_PASSWORD_PAIRS)
# auth_overview = BasicAuth(interface.interface, VALID_USERNAME_PASSWORD_PAIRS)

# auth_home = dash_auth.BasicAuth(index.index, VALID_USERNAME_PASSWORD_PAIRS)
# auth_overview = dash_auth.BasicAuth(interface.interface, VALID_USERNAME_PASSWORD_PAIRS)


@app.route("/overview")
def redirecionar_home():
    return interface.interface.index()


@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        # Obter os dados do formulário enviado pela interface Dash
        nome = request.form['username-input']
        empresa = request.form['company-input']
        email = request.form['email-input']
        senha = request.form['password-input']

        # Criar um novo objeto UsuarioSistema com os dados recebidos
        novo_usuario = UsuarioSistema(
            nome_usuario=nome,
            nome_empresa=empresa,
            email_login=email,
            senha_login=senha
        )
        # Adicionar o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        # Retornar uma resposta para a interface Dash
        return index.index.index()
    return cadastro.cadastro.index()


@app.route('/')
def redireciona_inicio():
    return pagina_inicial.inicial.index()
