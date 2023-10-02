import json
from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from app.templates.partials.index import sidebar, navbar

df = pd.read_csv(r"app\files\saida_atualizado.csv")

# Lê os nomes das usinas da coluna "name"
usina_names = df['name'].tolist()

lista = Dash(__name__, server=app, external_stylesheets=[dbc.themes.LUX], url_base_pathname="/lista/")
lista.layout = dbc.Container(
    [
        # Navbar
        navbar,
        
        dbc.Row([
            dbc.Col([], sm=3),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            html.H1("Lista de Usinas", className='prod-u'),
                            html.Ul([
                                html.Li(name, className='prod-u') for name in usina_names
                            ])
                        ])
                    ], color='dark', className='crd bg-grey'),
                ]),
            ], sm=6),
            dbc.Col([], sm=3),
        ], className="mt-4"),
    ],
    fluid=True,
)