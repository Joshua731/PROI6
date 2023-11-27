import dash_auth
import pandas as pd
from dash import Dash, html, dcc, Input, Output
from sqlalchemy import create_engine

from app import app
import dash_bootstrap_components as dbc

from app.templates.partials.index import get_local_ip

inicial = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname='/')
inicial.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sm=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Seja bem-vindo ao Dashua! Cadastre-se para continuar'),
                dbc.CardBody([
                    dbc.ButtonGroup([
                        # dbc.Button('Entrar', href=f'http://{get_local_ip()}:5001/home', color='dark'),
                        dbc.Button('Cadastrar', href=f'http://{get_local_ip()}:5001/cadastro-1', color='dark')
                    ])
                ])
            ], color='dark', class_name='card-home')
        ], sm=6),
        dbc.Col(sm=3),
    ])
], fluid=True)

