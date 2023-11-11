import dash

from app import app
from dash import Dash, dcc, html, Input, Output
from app.templates.partials.index import sidebar, navbar, caminho_http
import dash_bootstrap_components as dbc

cad_banco_1 = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app, url_base_pathname='/formulario_db/')
cad_banco_1.layout = dbc.Container([
    # Navbar
    dbc.Row([
        navbar,
        dcc.Location(id='url', refresh=False),
    ]),
    # Conteúdo da página
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Cadastrar banco de dados no sistema"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Input(id='input-db', placeholder='Nome da base de dados')
                            ])
                        ], sm=12)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Input(id='input-usuario', placeholder='Usuário')
                            ])
                        ], sm=6),
                        dbc.Col([
                            dbc.Row([
                                dbc.Input(id='input-senha', placeholder='Senha')
                            ])
                        ], sm=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Input(id='input-IP', placeholder='Endereço IP')
                            ])
                        ], sm=9),
                        dbc.Col([
                            dbc.Row([
                                dbc.Input(id='input-porta', placeholder='Porta')
                            ])
                        ], sm=3)
                    ]),
                ]),
                dbc.CardFooter(html.A('Registrar', id='red-pt-2'))
            ], class_name='card-db-form')
        ], sm=12),
    ])
], fluid=True)


@cad_banco_1.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname'),
)
def mostra_pagina(path):
    print(path)
    return path


@cad_banco_1.callback(
    Output('url', 'pathname'),
    Input('input-db', 'value'),
    Input('input-usuario', 'value'),
    Input('input-senha', 'value'),
    Input('input-IP', 'value'),
    Input('input-porta', 'value'),
    Input('red-pt-2', 'n_clicks'),
)
def redireciona(db, usuario, senha, IP, porta, n_cliques):
    if db and usuario and senha and IP and porta and dash.ctx.triggered_id == 'red-pt-2':
        return f'/formulario_db/2'
    else:
        return '/'
