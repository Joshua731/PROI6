import json
from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from app.templates.partials.index import sidebar, navbar

# Remove the code for reading the CSV file and creating the figures

lista = Dash(__name__, server=app, external_stylesheets=[dbc.themes.LUMEN], url_base_pathname="/lista/")
lista.layout = dbc.Container(
    [
        # Navbar
        navbar,
        
        dbc.Row([
            dbc.Col([
            ], sm=6),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.Row([
                            html.Fieldset([
                                dbc.Row([

                                ]),
                                dbc.Row([
                                    dbc.CardGroup([
                                        dbc.Card([
                                            dbc.CardBody([
                                            
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                
                                            ])
                                        ])
                                    ])
                                ])
                            ]),
                        ])

                    ], color='dark', className='crd'),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.Row([

                            ]),
                            dbc.Row([

                            ]),
                        ], color='dark', className='crd-g'),
                    ], sm=10),
                    dbc.Col([
                        dbc.Card([
                        ], color='dark', class_name='crd-i'),
                    ], sm=2)
                ])
            ], sm=6)
        ], className="mt-4"),
    ],
    fluid=True,
)