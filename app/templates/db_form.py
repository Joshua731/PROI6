from app import app
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

db_form = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app, url_base_pathname='/db_form/')
db_form.layout = dbc.Container([
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