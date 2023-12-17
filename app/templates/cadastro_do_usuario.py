from app import app
from app.templates.partials.index import navbar
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

cadastro_do_usuario = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app, url_base_pathname='/cadastro_usuario/')
cadastro_do_usuario.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Cadastrar novo usuário'),
                dbc.Card([
                    dbc.Row([
                        dbc.Col([
                            html.P('Bem vindo! Essa é a ')
                        ], sm=12)
                    ])
                ])
            ])
        ], sm=12)
    ])
], fluid=True)
