import dash
import pandas as pd
import requests
import sqlalchemy
from dash.exceptions import PreventUpdate
from sqlalchemy import create_engine

from app import app
from dash import Dash, dcc, html, Input, Output
from app.templates.partials.index import navbar, caminho_http
import dash_bootstrap_components as dbc

estados = [
    {'label': 'Acre', 'value': 'AC'},
    {'label': 'Alagoas', 'value': 'AL'},
    {'label': 'Amapá', 'value': 'AP'},
    {'label': 'Amazonas', 'value': 'AM'},
    {'label': 'Bahia', 'value': 'BA'},
    {'label': 'Ceará', 'value': 'CE'},
    {'label': 'Distrito Federal', 'value': 'DF'},
    {'label': 'Espírito Santo', 'value': 'ES'},
    {'label': 'Goiás', 'value': 'GO'},
    {'label': 'Maranhão', 'value': 'MA'},
    {'label': 'Mato Grosso', 'value': 'MT'},
    {'label': 'Mato Grosso do Sul', 'value': 'MS'},
    {'label': 'Minas Gerais', 'value': 'MG'},
    {'label': 'Pará', 'value': 'PA'},
    {'label': 'Paraíba', 'value': 'PB'},
    {'label': 'Paraná', 'value': 'PR'},
    {'label': 'Pernambuco', 'value': 'PE'},
    {'label': 'Piauí', 'value': 'PI'},
    {'label': 'Rio de Janeiro', 'value': 'RJ'},
    {'label': 'Rio Grande do Norte', 'value': 'RN'},
    {'label': 'Rio Grande do Sul', 'value': 'RS'},
    {'label': 'Rondônia', 'value': 'RO'},
    {'label': 'Roraima', 'value': 'RR'},
    {'label': 'Santa Catarina', 'value': 'SC'},
    {'label': 'São Paulo', 'value': 'SP'},
    {'label': 'Sergipe', 'value': 'SE'},
    {'label': 'Tocantins', 'value': 'TO'}
]

df_banco = None
engine = None

df = pd.read_csv(r'app\files\saida_atualizado.csv')

cad_banco_1 = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app, url_base_pathname='/cadastro-1/')
cad_banco_1.layout = dbc.Container([
    # Navbar
    dbc.Row([
        navbar,
        dcc.Location(id='url', refresh=False),
    ]),
    # Conteúdo da página
    dbc.Row([
        dbc.Col([
            dbc.Tabs(id='tabs-cad', active_tab='cad-usuario', children=[
                dbc.Tab(label='Usuário', tab_id='cad-usuario', children=[
                    dbc.Row([
                        dbc.Col([], sm=3),
                        dbc.Col([
                            dbc.Row([
                                dbc.Card([
                                    dbc.CardHeader('Cadastro do Usuário', class_name='card-title'),
                                    dbc.CardBody([
                                        html.Label("Nome Completo"),
                                        dcc.Input(type="text", id="username-input", placeholder="Entre com seu Usuario",
                                                  className="form-control"),
                                        html.Label('Empresa'),
                                        dcc.Input(type="text", id="company-input",
                                                  placeholder="Entre com a sua Empresa",
                                                  className="form-control"),
                                        html.Label('Email'),
                                        dcc.Input(type="email", id="email-input", placeholder="Entre com o seu Email",
                                                  className="form-control"),
                                        html.Label("Senha"),
                                        dcc.Input(type="password", id="password-input",
                                                  placeholder="Entre com a sua Senha",
                                                  className="form-control"),

                                        html.Div(id="signup-message", className="mt-3"),
                                    ]),
                                ], color='dark', className='crd'),
                            ]),
                        ], sm=6),
                        dbc.Col([], sm=3),
                    ], className="mt-4"),
                ]),
                dbc.Tab(label='Banco', tab_id='cad-db', children=[
                    dbc.Row([
                        dbc.Col(sm=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Integração da fonte de dados"),
                                dbc.CardBody([
                                    dbc.Row([
                                        dcc.Dropdown(
                                            id='drop-origem',
                                            placeholder='Origem dos dados',
                                            options=[
                                                {"label": 'MySQL', 'value': 'mysql'},
                                                {'label': 'SQL Server', 'value': 'sql-server'},
                                            ],
                                            style={'background-color': 'rgb(7,54,66)',
                                                   'placeholder': {'color': 'white'}},
                                        )
                                    ]),
                                    dbc.Row(id='conteudo-origem'),
                                ])
                            ], color='dark')
                        ], sm=6),
                        dbc.Col(sm=3),
                    ])
                ]),
                dbc.Tab(tab_id='sel-cols', label='Colunas', children=[
                    dbc.Row([
                        dbc.Col(sm=2),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Tabs(id='tabs-cols-db', active_tab='tab-invs', children=[
                                        dbc.Tab(tab_id='tab-invs', label='Inversores', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checkbox(
                                                        id='check-invs',
                                                        label='Possui Inversores? (caso não possuir, apenas ignore)',
                                                        value=False,
                                                    )
                                                ], sm=12)
                                            ])
                                        ]),
                                        dbc.Tab(tab_id='tab-cm', label='Central Meteorológica', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checkbox(
                                                        id='check-cm',
                                                        label='Possui Central Meteorológica? (caso não possuir, apenas ignore)',
                                                        value=False,
                                                    )
                                                ], sm=12)
                                            ])
                                        ]),
                                        dbc.Tab(tab_id='tab-idgt', label='IDGT', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checkbox(
                                                        id='check-idgt',
                                                        label='Possui Índice de Desempenho? (caso não possuir, apenas ignore)',
                                                        value=False,
                                                    )
                                                ], sm=12)
                                            ])
                                        ]),
                                        dbc.Tab(tab_id='tab-qgbt', label='QGBT', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checkbox(
                                                        id='check-qgbt',
                                                        label='Possui Quadro Geral de Baixa Tensão? (caso não possuir, apenas ignore)',
                                                        value=False,
                                                    )
                                                ], sm=12)
                                            ]),
                                        ]),
                                        dbc.Tab(tab_id='tab-irrad-pot', label='Irradiância x Potência', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Card([
                                                        dbc.CardHeader('Irradiância'),
                                                        dbc.CardBody([
                                                            dbc.Checkbox(
                                                                id='check-irrad',
                                                                label='Possui Irradiância? (caso não possuir, apenas ignore)',
                                                                value=False,
                                                            )
                                                        ])
                                                    ], color='dark')
                                                ], sm=6),
                                                dbc.Col([
                                                    dbc.Card([
                                                        dbc.CardHeader('Potência'),
                                                        dbc.CardBody([
                                                            dbc.Checkbox(
                                                                id='check-pot',
                                                                label='Possui Potência Ativa? (caso não possuir, apenas ignore)',
                                                                value=False,
                                                            )
                                                        ])
                                                    ], color='dark')
                                                ], sm=6),
                                            ])
                                        ]),
                                        dbc.Tab(tab_id='prod-data', label='Energia/Data', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checkbox(
                                                        id='check-prod',
                                                        label='Possui Energia Injetada? (caso não possuir, apenas ignore)',
                                                        value=False,
                                                    ),
                                                ])
                                            ]),
                                        ])
                                    ])
                                ]),
                            ], color='dark'),
                        ], sm=8),
                        dbc.Col(sm=2),
                    ]),
                ]),
                dbc.Tab(tab_id='tab-usinas', label='Usinas', children=[
                    dbc.Row([
                        dbc.Col(sm=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='drop-estado',
                                                options=[{'label': 'São Paulo', 'value': 'SP'}],
                                                placeholder='Selecione o(s) estado(s) da(s) usina(s)',
                                                multi=True,
                                                style={'background-color': 'rgb(7,54,66)'},
                                            )
                                        ], sm=6),
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='drop-cidade',
                                                options=[{'label': cidade, 'value': cidade} for cidade in df['name']],
                                                placeholder='Selecione a(s) cidade(s) da(s) usina(s)',
                                                multi=True,
                                                style={'background-color': 'rgb(7,54,66)'},
                                            )
                                        ], sm=6)
                                    ])
                                ])
                            ], color='dark'),
                        ], sm=6),
                        dbc.Col(sm=3),
                    ])

                ])
            ]),
        ], sm=12),
    ]),

], fluid=True)


@cad_banco_1.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname'),
)
def mostra_pagina(path):
    print(path)
    return path


# @cad_banco_1.callback(
#

# )
# def redireciona(db, usuario, senha, IP, porta, n_cliques):
#     if dash.ctx.triggered_id == 'red-pt-2':
#         url = f'http://{caminho_http}/cadastro'  # URL da rota do Flask
#         data = {'db': db, 'usuario_db': usuario, 'senha_db': senha, 'IP_db': IP, 'porta_db': porta}
#
#         response = requests.post(url, data=data)  # Envia os dados para o Flask
#         return response.text  # Exibe a mensagem de resposta do Flask na interface Dash


@cad_banco_1.callback(
    Output("conteudo-origem", "children"),
    Input('drop-origem', 'value')
)
def mostrar_dados_pelo_tipo_de_cadastro(tipo):
    if tipo is None:
        raise PreventUpdate
    if tipo in ['mysql', 'sql-server']:
        return dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-db', placeholder='Nome da base de dados',
                                  type='text')
                    ])
                ], sm=12),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-usuario', placeholder='Usuário', type='text')
                    ])
                ], sm=6),
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-senha', placeholder='Senha', type='password')
                    ])
                ], sm=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-IP', placeholder='Endereço IP', type='text')
                    ])
                ], sm=9),
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-porta', placeholder='Porta', type='number')
                    ])
                ], sm=3)
            ]),
            dbc.Row(id='status-banco'),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Confirma', id='red-cols', color='dark')
                ], sm=2)
            ]),
        ], sm=12)
    if not tipo in ['mysql', 'sql-server']:
        return html.P('Estamos trabalhando nessa funcionalidade')


@cad_banco_1.callback(
    Output('tabs-cad', 'active_tab'),
    Output('status-banco', 'children'),
    Input('drop-origem', 'value'),
    Input('input-db', 'value'),
    Input('input-usuario', 'value'),
    Input('input-senha', 'value'),
    Input('input-IP', 'value'),
    Input('input-porta', 'value'),
    Input('red-cols', 'n_clicks'),
)
def redireciona_para_colunas(tipo, base, usuario, senha, ip, porta, botao):
    global df_banco, engine
    if dash.ctx.triggered_id == 'red-cols':
        if tipo == 'sql-server':
            query = '''
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
            '''
            try:
                engine = create_engine(
                    f'mssql+pyodbc://{usuario}:{senha}@{ip}:{porta}/{base}?driver=ODBC+Driver+17+for+SQL+Server')
                return 'sel-cols', html.P('OK')
            except Exception as e:
                print(e)
                return 'cad-db', html.P(e)
    raise PreventUpdate
