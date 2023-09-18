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
            brand_href="#",
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Perfil", href="/page-2")),
                dbc.NavItem(dbc.NavLink("Configurações", href="/page-3")),
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
        dbc.NavbarSimple(
            brand="Bem-vindo a S.D.H.",
            brand_href="#",
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Perfil", href="/page-2")),
                dbc.NavItem(dbc.NavLink("Configurações", href="/page-3")),
            ],
        ),
    ],
)
    
content = html.Div(id="page-content")
header = html.H4(
    "Side Example.py", className="bg-primary text-white p-2 mb-2 text-center"
)