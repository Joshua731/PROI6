import json
from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np

navbar = html.Div([
        dbc.NavbarSimple(
            brand="Bem-vindo a S.D.H.",
            brand_href="http://127.0.0.1:5000/",
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="http://127.0.0.1:5000/")),
                dbc.NavItem(dbc.NavLink("Mapa", href="http://127.0.0.1:5000/interface")),
                dbc.NavItem(dbc.NavLink("Lista", href="http://127.0.0.1:5000/lista")),
                dbc.NavItem(dbc.NavLink("Login", href="http://127.0.0.1:5000/login")),
            ],
        ),
    ],
)

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        navbar,
    ],
)
    
content = html.Div(id="page-content")
header = html.H4(
    "Side Example.py", className="bg-primary text-white p-2 mb-2 text-center"
)