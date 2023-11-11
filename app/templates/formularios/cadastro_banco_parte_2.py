from app import app
from app.templates.partials.index import navbar
from dash import Dash, dcc, html, Input, Output, State
import dash
import dash_bootstrap_components as dbc

cad_banco_2 = dbc.Container([
    dbc.Row([
        navbar
    ]),
    dbc.Row([
        dbc.Card([
            dbc.CardHeader('Selecionar tabelas'),
            dbc.CardBody([
                dbc.Row([
                    html.H6('Tabelas disponíveis')
                ]),
                dbc.Row([
                    dcc.Dropdown(
                        options=[{}]
                    )
                ])
            ])
        ])
    ])
], fluid=True)
