import sqlite3
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask, redirect, request, session
import jwt
import datetime
import functools
from flask import request, redirect

SECRET_KEY = "shua10!"


def login_required(view_func):
    @functools.wraps(view_func)
    def wrapped_view(*args, **kwargs):
        token = request.cookies.get("jwt_token")
        if not token:
            # Redirecionar para a página de login se o token não estiver presente
            return pagina_login.index()

        # Verificar o token
        usuario = verificar_token(token)
        if not usuario:
            # Redirecionar para a página de login se o token for inválido
            return pagina_login.index()

        # O usuário possui um token válido, permitir o acesso à página
        return view_func(*args, **kwargs)

    return wrapped_view


def gerar_token(usuario):
    expiracao = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {
        "usuario": usuario,
        "exp": expiracao
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["usuario"]
    except jwt.ExpiredSignatureError:
        # O token expirou
        return None
    except jwt.InvalidTokenError:
        # Token inválido
        return None


pop_up = dbc.Modal([
    dbc.ModalHeader("Erro de Login"),
    dbc.ModalBody("Nome de usuário ou senha incorretos"),
    dbc.ModalFooter(dbc.Button("Fechar", id="btn-fechar-popup", color="primary"))
],
    id="login-popup",
    centered=True,
    is_open=False
)


def salvar_informacoes(nome, nascimento, email, genero, idioma):
    # Suponhamos que temos um arquivo chamado 'perfil.db' para o SQLite
    conn = sqlite3.connect('perfil.db')
    cursor = conn.cursor()

    # Crie uma tabela chamada 'perfil' se ela ainda não existir
    cursor.execute('''CREATE TABLE IF NOT EXISTS perfil
                      (nome TEXT, nascimento TEXT, email TEXT, genero TEXT, idioma TEXT)''')

    # Insira as informações do perfil na tabela
    cursor.execute("INSERT INTO perfil (nome, nascimento, email, genero, idioma) VALUES (?, ?, ?, ?, ?)",
                   (nome, nascimento, email, genero, idioma))

    # Salve as alterações e feche a conexão com o banco de dados
    conn.commit()
    conn.close()

    # Redirecione para a página de perfil após salvar com sucesso
    return perfil.index()


# Inicializando o servidor Flask
servidor = Flask(__name__)
# Layout do painel
painel = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR, dbc.icons.FONT_AWESOME], server=servidor,
              url_base_pathname='/painel/')

painel.layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink(
                        dbc.Row([
                            dbc.Col(html.I(className="fas fa-user-circle fa-2x", id='icone-usuario'), sm=2),
                            dbc.Col(html.P("Usuário Anônimo", className='nome-usuario'), sm=10),
                        ], className='row-usuario', align='center'),
                        className='navlink-usuario',
                        href="/perfil",
                        external_link=True
                    )),
                    dbc.NavItem(
                        dbc.NavLink(
                            dbc.Row([
                                dbc.Col(html.I(className="icone-usuario fas fa-cog fa-1x"), sm=2),
                                dbc.Col(html.P("Configurações", className='nome-usuario'), sm=10),
                            ], className='row-usuario', align='center'),
                            href="/configuracoes"
                        ),
                    ),
                ],
                vertical=True,
                pills=True,
            ),
            sm=2
        ),
        dbc.Col(sm=2),
    ]),
    dbc.Row(dbc.Col(sm=10)),
    dcc.Location(id="redirecionar-painel", refresh=False)
], className='div-panel')

# Layout do perfil do usuário
perfil = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR, dbc.icons.FONT_AWESOME], server=servidor,
              url_base_pathname='/perfil/')

perfil.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(src="assets/usuario.png", className="img-profile img-responsive rounded-circle"),
            html.H3("Nome do Usuário", className="profile-name profile-red-text"),
            html.P("Usuário Anônimo", className="profile-username"),
            html.P("Data de Nascimento: 01/01/1990", className="profile-info"),
            html.P("E-mail: usuario@email.com", className="profile-info"),
            html.P("Gênero: Masculino", className="profile-info"),
            html.P("Preferências de Idioma: Português", className="profile-info"),
            html.A("Editar", id="btn-editar", className="edit-button",
                   href='/editar-perfil/', target="_self"),

        ], sm=4, className="profile-info-container mt-3"),  # Adicionando margem superior (mt-3)
        dbc.Col([
            html.H3("Biografia", className="profile-heading mt-3 profile-red-text"),
            # Adicionando margem superior (mt-3)
            html.P("Essa é uma breve descrição do usuário. "
                   "Ele pode escrever sobre seus interesses, hobbies ou qualquer coisa relevante.",
                   className="profile-bio"),
            html.Hr(),
            html.H3("Histórico de Atividades", className="profile-heading mt-3 profile-red-text"),
            # Adicionando margem superior (mt-3)
            html.Ul([
                html.Li("Ação 1 - Data e hora"),
                html.Li("Ação 2 - Data e hora"),
                html.Li("Ação 3 - Data e hora"),
            ], className="activity-list"),
        ], sm=8, className="profile-activity-container mt-3"),
    ]),

    # Adicionando margem superior (mt-3)
], fluid=True, id="profile-page", className='container-fluid')


# Rota Flask para a página principal
@servidor.route("/painel")
@login_required
def redirecionar_para_painel():
    token = request.cookies.get("jwt_token")
    if not token:
        return pagina_login.index()

    usuario = verificar_token(token)
    if usuario:
        return painel.index()

    # Token inválido ou expirado, redirecionar para a página de login
    return pagina_login.index()


@servidor.route("/")
def redirecionar_para_login():
    return pagina_login.index()


edicao_perfil = Dash(__name__, server=servidor, external_stylesheets=[dbc.themes.VAPOR],
                     url_base_pathname='/editar-perfil/')

edicao_perfil.layout = dbc.Container([
    html.H1("Editar Perfil", className="titulo-editar"),
    dbc.Row([
        dbc.Col([
            dbc.Label("Nome do Usuário", className="label-editar"),
            dbc.Input(id="input-nome", type="text", value="Usuário Anônimo", className="input-editar"),
            dbc.Label("Data de Nascimento", className="label-editar"),
            dbc.Input(id="input-nascimento", type="text", value="01/01/1990", className="input-editar"),
            dbc.Label("E-mail", className="label-editar"),
            dbc.Input(id="input-email", type="email", value="usuario@email.com", className="input-editar"),
            dbc.Label("Gênero", className="label-editar"),
            dcc.Dropdown(
                id="dropdown-genero",
                options=[
                    {"label": "Masculino", "value": "M"},
                    {"label": "Feminino", "value": "F"},
                    {"label": "Outro", "value": "O"},
                ],
                value="M",
                className="dropdown-editar",
            ),
            dbc.Label("Preferências de Idioma", className="label-editar"),
            dcc.Textarea(id="textarea-idioma", value="Português", style={"width": "100%"}, className="textarea-editar"),
            dbc.Button("Salvar", id="btn-salvar", color="primary", className="mt-3 btn-editar"),
        ], sm=6),
        dbc.Col([
            html.Div(id="div-salvo"),
        ], sm=6),
    ]),
], fluid=True, className='container-fluid')


# Callback para exibir mensagem de sucesso ao salvar as informações
@edicao_perfil.callback(Output("div-salvo", "children"),
                        Input("btn-salvar", "n_clicks"),
                        State("input-nome", "value"), State("input-nascimento", "value"),
                        State("input-email", "value"), State("dropdown-genero", "value"),
                        State("textarea-idioma", "value"))
def salvar_e_redirecionar(n_clicks, nome, nascimento, email, genero, idioma):
    botao = dash.ctx.triggered_id
    if botao == 'btn-salvar':
        return salvar_informacoes(nome, nascimento, email, genero, idioma)
    raise PreventUpdate


@servidor.route("/editar-perfil/")
@login_required
def redirecionar_para_edicao_perfil():
    token = request.cookies.get("jwt_token")
    if not token:
        return pagina_login.index()

    usuario = verificar_token(token)
    if usuario:
        return edicao_perfil.index()

    # Token inválido ou expirado, redirecionar para a página de login
    return pagina_login.index()


# Inicializando o aplicativo Dash
pagina_login = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR], server=servidor,
                         url_base_pathname='/')


# Função para verificar o login
def verificar_login(usuario, senha):
    # Suponhamos que temos um arquivo chamado 'usuarios.db' para o SQLite
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Verifique se o usuário e a senha correspondem
    cursor.execute("SELECT * FROM usuarios WHERE nome_usuario=? AND senha=?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        # Login bem-sucedido, retornar token JWT
        return gerar_token(usuario)

    return None


pagina_login.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="Login", tab_id="login-tab", className='tab-style'),
                dbc.Tab(label="Cadastro", tab_id="cadastro-tab", className='tab-style'),
            ],
                id="tabs",
                active_tab="login-tab"),
        ], sm=12)
    ]),
    dbc.Row([
        dbc.Col([], id='tabs-content', width=12, className="tabs-content-container"),
        # Use a classe CSS para centralizar
    ]),
    dbc.Row([
        pop_up
    ])
], fluid=True, className="container-fluid")

# Definindo o tamanho e a responsividade dos cards de Login e Cadastro
login_card = dbc.Card([
    dbc.CardHeader("Login", className="login-card-header"),
    dbc.CardBody([
        dbc.Form([
            dbc.Label("Nome de Usuário", className="login-label"),
            dbc.Input(id="input-usuario", type="text", placeholder="Digite seu nome de usuário"),
        ]),
        dbc.Form([
            dbc.Label("Senha", className="login-label"),
            dbc.Input(id="input-senha", type="password", placeholder="Digite sua senha"),
        ]),
        dbc.Button("Entrar", id="btn-entrar", color="light", className="login-button mt-3"),
    ]),
], className="login-card fade-in")  # Tons de roxo mais claro

cadastro_card = dbc.Card([
    dbc.CardHeader("Cadastro", className="login-card-header"),
    dbc.CardBody([
        dbc.Form([
            dbc.Label("Nome de Usuário", className="login-label"),
            dbc.Input(id="input-novo-usuario", type="text", placeholder="Digite seu nome de usuário"),
        ]),
        dbc.Form([
            dbc.Label("Senha", className="login-label"),
            dbc.Input(id="input-nova-senha", type="password", placeholder="Digite sua senha"),
        ]),
        dbc.Button("Cadastrar", id="btn-cadastrar", color="light", className="cadastrar-button mt-3"),
    ]),
], className="login-card", style={"background-color": "#d1c4e9"})  # Tons de roxo mais claro

login_layout = dbc.Col(login_card, sm=4)  # Tamanho do card de login (4/12)
cadastro_layout = dbc.Col(cadastro_card, sm=4)  # Tamanho do card de cadastro (4/12)


@pagina_login.callback(
    Output("login-popup", "is_open"),
    # Output("tabs-content", "children"),
    Input("btn-fechar-popup", "n_clicks"),
    Input("btn-entrar", "n_clicks"),
    State("input-usuario", "value"),
    State("input-senha", "value"),
    prevent_initial_call=True,
)
def controlar_pop_up(fechar_clicks, entrar_clicks, usuario, senha):
    # Controla a exibição do modal
    ctx = dash.callback_context

    if not ctx.triggered:
        # Nenhum botão foi clicado, mantém o estado de exibição padrão
        return False

    botao_clicado = ctx.triggered[0]["prop_id"].split(".")[0]

    if botao_clicado == "btn-entrar" and usuario and senha:
        if not verificar_login(usuario, senha):
            # Exibe o modal
            return True

    # Se o botão "X" (fechar) foi clicado ou o login foi bem-sucedido, esconde o modal
    return False


@servidor.route("/perfil")
@login_required
def perfil():
    token = request.cookies.get("jwt_token")
    if not token:
        return pagina_login.index()

    usuario = verificar_token(token)
    if usuario:
        return perfil.index()

    # Token inválido ou expirado, redirecionar para a página de login
    return pagina_login.index()


def cadastrar_usuario(usuario, senha):
    # Suponhamos que temos um arquivo chamado 'usuarios.db' para o SQLite
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Verifique se o usuário já existe
    cursor.execute("SELECT * FROM usuarios WHERE nome_usuario=?", (usuario,))
    resultado = cursor.fetchone()
    if resultado:
        # Usuário já existe, não é possível cadastrar novamente
        conn.close()
        return False

    # Cadastre o novo usuário
    cursor.execute("INSERT INTO usuarios (nome_usuario, senha) VALUES (?, ?)", (usuario, senha))
    conn.commit()
    conn.close()

    # Cadastro bem-sucedido, retornar token JWT
    return gerar_token(usuario)


@pagina_login.callback(Output("btn-entrar", "href"),
                       Input("btn-entrar", "n_clicks"),
                       Input("btn-cadastrar", "n_clicks"),
                       State("input-usuario", "value"),
                       State("input-senha", "value"),
                       State("input-novo-usuario", "value"),
                       State("input-nova-senha", "value"))
def redirecionar_apos_login_ou_cadastro(n_clicks_login, n_clicks_cadastro, usuario, senha, novo_usuario, nova_senha):
    botao_atual = dash.ctx.triggered_id
    if botao_atual == 'btn-entrar':
        token = verificar_login(usuario, senha)
        if token:
            # Configurar o token JWT como um cookie para autenticação
            response = pagina_login.index()
            response.set_cookie("jwt_token", token)
            return edicao_perfil.index()

    if botao_atual == 'btn-cadastrar':
        token = cadastrar_usuario(novo_usuario, nova_senha)
        if token:
            # Configurar o token JWT como um cookie para autenticação
            response = pagina_login.index()
            response.set_cookie("jwt_token", token)
            # Redirecionar para o painel após o cadastro bem-sucedido
            return edicao_perfil.index()

    # Não redirecionar
    raise PreventUpdate


# Callback para controlar o conteúdo do tab e aplicar animação de deslizamento
@pagina_login.callback(
    Output("tabs-content", "children"),
    Output("tabs-content", "classname"),
    Input("tabs", "active_tab"),
    prevent_initial_call=True,
)
def update_tab_content(active_tab):
    # Controle do conteúdo com base no tab ativo
    if active_tab == "login-tab":
        return login_layout, {"animation-name": "slide-in-right"}  # Animar da direita para a esquerda
    elif active_tab == "cadastro-tab":
        return cadastro_layout, {"animation-name": "slide-in-left"}  # Animar da esquerda para a direita


if __name__ == "__main__":
    servidor.run(debug=True)
