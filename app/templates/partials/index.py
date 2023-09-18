import json
from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np

navbar = 
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