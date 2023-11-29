import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc, Input, Output
from sqlalchemy import create_engine

from app.configs import db
from app.templates.cadastros.base_de_dados import nova_database

from app import app

engine = create_engine('sqlite:///./database/database.db')

cm = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app, url_base_pathname='/cadastro/colunas/cm/')
cm.layout = dbc.Container([
    html.H6('Hello World!')
])
