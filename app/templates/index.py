import dash_auth
import pandas as pd
from sqlalchemy import create_engine

from app import app
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from app.templates.partials.index import navbar

title = None
index = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname='/home/')
index.title = f'{title} - Dashua' if title else 'Welcome to Dashua'
user = {'username': 'Joshua'}
index.layout = dbc.Container(
    [
        navbar,
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col([], sm=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Dashua", className="card-title"),
                        html.H5("Seja bem vindo ao Dashua."),
                        html.P("Análise em tempo real de dados remetentes a energia solar."),
                        # dbc.Button('Logout', href=f'http://{get_local_ip()}:5000/logout')
                    ])
                ], color='dark', className='crd mx-auto bg-grey'),
            ], sm=6),
            dbc.Col([], sm=3)
        ], className="mt-4"),
    ],
    fluid=True,
)


@index.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path
