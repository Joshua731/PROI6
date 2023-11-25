# import dash
# from flask import Flask, request, jsonify, render_template_string, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# import jwt
# import dash_bootstrap_components as dbc

# app_flask = Flask(__name__)
# app = dash.Dash(__name__, server=app_flask, url_base_pathname='/dash/', external_stylesheets=[dbc.themes.SOLAR])

# app_flask.config['SECRET_KEY'] = 'sua_chave_secreta'
# app.server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#
# db = SQLAlchemy(app_flask)
# login_manager = LoginManager(app_flask)
# login_manager.login_view = 'login'


# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# def generate_token(user):
#     token = jwt.encode({'username': user.username}, app_flask.config['SECRET_KEY'], algorithm='HS256')
#     return token


# @app_flask.route('/get_token', methods=['POST'])
# def get_token():
#     username = request.json.get('username')
#     password = request.json.get('password')
#
#     user = User.query.filter_by(username=username).first()
#     if user and user.password == password:
#         token = generate_token(user)
#         return jsonify({'token': token.decode('UTF-8')})
#
#     return jsonify({'message': 'Credenciais inválidas'}), 401


# @app_flask.route('/dash/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             token = generate_token(user)
#             return jsonify({'token': token.decode('UTF-8')})
#
#         return jsonify({'message': 'Credenciais inválidas'}), 401
#
#     return render_template_string('''
#         <h1>Login</h1>
#         <form method="post">
#             <input type="text" placeholder="Username" name="username"><br>
#             <input type="password" placeholder="Password" name="password"><br>
#             <input type="submit" value="Login">
#         </form>
#     ''')


# @app_flask.route('/dash/home')
# def dash_home():
#     token = request.headers.get('Authorization')
#     if not token:
#         return jsonify({'message': 'Token não encontrado'}), 401
#
#     try:
#         decoded_token = jwt.decode(token, app_flask.config['SECRET_KEY'], algorithms=['HS256'])
#         username = decoded_token['username']
#         user = User.query.filter_by(username=username).first()
#         if not user:
#             raise jwt.InvalidTokenError
#
#         return render_template_string('<h1>Welcome to the home page! <a href="/logout">Logout</a></h1>')
#
#     except jwt.ExpiredSignatureError:
#         return jsonify({'message': 'Token expirado'}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({'message': 'Token inválido'}), 401


# @app_flask.route('/')
# def home():
#     if current_user.is_authenticated:
#         return redirect('/dash/home')
#     return render_template_string('<h1>Welcome to the application! Please <a href="/dash/login">login</a> or <a href="/dash/cadastro">sign up</a>.</h1>')


# @app_flask.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('/dash/')


# @app_flask.route('/dash/')
# def dash_redirect():
#     return redirect('/dash/login')


# @app_flask.route('/dash/cadastro', methods=['GET', 'POST'])
# def cadastro():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         new_user = User(username=username, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#
#         return redirect('/dash/login')
#
#     return render_template_string('''
#         <h1>Cadastro</h1>
#         <form method="post">
#             <input type="text" placeholder="Username" name="username"><br>
#             <input type="password" placeholder="Password" name="password"><br>
#             <input type="submit" value="Cadastrar">
#         </form>
#     ''')


# if __name__ == '__main__':
#     with app_flask.app_context():
#         db.create_all()
#     app_flask.run(debug=True)

import requests


def get_external_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Falha ao obter o IP externo."
    except requests.RequestException as e:
        return f"Erro de conexão: {e}"


# ip_externo = get_external_ip()
# print(f"Seu IP externo é: {ip_externo}")
#
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_auth
#
# # Usuários autorizados
# VALID_USERNAME_PASSWORD_PAIRS = {
#     'username': 'password',
#     'admin': 'admin'
# }
#
# app = dash.Dash(__name__)
#
# # Definindo a página de layout
# app.layout = html.Div([
#     html.H1('Página Protegida'),
#     dcc.Location(id='url_login', refresh=True),
#     html.Div(id='page-content')
# ])
#
#
# # Definindo o layout da página de login
# def login_layout():
#     return html.Div([
#         html.H2('Por favor, faça o login'),
#         dcc.Input(id='username', type='text', placeholder='Usuário'),
#         dcc.Input(id='password', type='password', placeholder='Senha'),
#         html.Button('Login', id='login-button'),
#         html.Div(id='login-output')
#     ])
#
#
# # Callback para autenticar o usuário
# @app.callback(
#     dash.dependencies.Output('page-content', 'children'),
#     [dash.dependencies.Input('url_login', 'pathname')]
# )
# def display_page(pathname):
#     if pathname == '/login':
#         return login_layout()
#     else:
#         return '404 Página não encontrada.'
#
#
# # Callback para verificar as credenciais
# @app.callback(
#     dash.dependencies.Output('login-output', 'children'),
#     [dash.dependencies.Input('login-button', 'n_clicks')],
#     [dash.dependencies.State('username', 'value'),
#      dash.dependencies.State('password', 'value')]
# )
# def authenticate(n_clicks, username, password):
#     if n_clicks is not None:
#         if (username in VALID_USERNAME_PASSWORD_PAIRS) and (password == VALID_USERNAME_PASSWORD_PAIRS[username]):
#             return dcc.Link('Clique para acessar a página protegida', href='/page_protegida')
#         else:
#             return html.Div('Credenciais inválidas. Tente novamente.')
#
#
# # Autenticação com dash_auth.BasicAuth
# auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
#
# if __name__ == '__main__':
#     app.run_server(debug=True)

# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.exceptions import PreventUpdate
# import dash_bootstrap_components as dbc
#
# # Inicializando o aplicativo Dash
# app = dash.Dash(__name__)
#
# # Layout da primeira página
# page_1_layout = html.Div([
#     html.H1('Página 1'),
#     html.Button('Ir para Página 2', id='btn-redirect')
# ])
#
# # Layout da segunda página
# page_2_layout = html.Div([
#     html.H1('Página 2'),
#     html.Button('Voltar para Página 1', id='btn-back')
# ])
#
# # Layout inicial do aplicativo
# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])
#
#
# # Callback para redirecionamento para página 2
# @app.callback(Output('url', 'pathname'), [Input('btn-redirect', 'n_clicks'), Input('btn-back', 'n_clicks')])
# def redirect_to_page(n_clicks_redirect, n_clicks_back):
#     if n_clicks_redirect is None and n_clicks_back is None:
#         raise PreventUpdate
#
#     if n_clicks_redirect is not None:
#         return '/page-2'
#     elif n_clicks_back is not None:
#         return '/'
#
#
#
# # Callback para renderizar a página correta com base na URL
# @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/':
#         return page_1_layout
#     elif pathname == '/page-2':
#         return page_2_layout
#     else:
#         return '404 - Página não encontrada'
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)

# import dash
# from dash import html
# from dash_auth import BasicAuth
# from flask import Flask
#
# server = Flask(__name__)
#
# # Primeira aplicação Dash com autenticação
# app1 = dash.Dash(__name__, server=server, url_base_pathname='/app1/')
# app1.layout = html.Div("Aplicação 1")
#
# # Configuração das credenciais para autenticação
# VALID_USERNAME_PASSWORD_PAIRS = {'username': 'password'}
#
# # Adiciona autenticação apenas à app1
# auth = BasicAuth(app1, VALID_USERNAME_PASSWORD_PAIRS)
#
# # Segunda aplicação Dash sem autenticação
# app2 = dash.Dash(__name__, server=server, url_base_pathname='/app2/')
# app2.layout = html.Div("Aplicação 2")
#
# if __name__ == '__main__':
#     server.run(host="0.0.0.0", debug=True, port=8050)

