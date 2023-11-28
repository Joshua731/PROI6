from app.configs import db
from dash import Dash, html, dcc, Input, Output
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc

cad_cols = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname='/cad-cols')
cad_cols.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Checkbox(
                    id='check-invs',
                    label='Possui Inversores? (caso não possuir, apenas ignore)',
                    value=False,
                )
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Próximo', color='dark', id='red-cm')
                ], sm=2)
            ])
        ], sm=12)
    ]),
    dbc.Row(id='row-invs'),
], fluid=True)

