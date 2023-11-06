import dash

from app import app
from dash import Dash, dcc, html, Input, Output
from app.templates.partials.index import sidebar, navbar
import dash_bootstrap_components as dbc

db_form = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app, url_base_pathname='/formulario_db/')
db_form.layout = dbc.Container([
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
                    dbc.Button('Registrar')
                ])
            ], class_name='card-db-form')
        ], sm=12),
    ])
], fluid=True)


@db_form.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname'),
)
def mostra_pagina(path):
    print(path)
    return path
