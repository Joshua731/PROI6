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
        color="dark",
        dark=True,
        children=[
            dbc.DropdownMenu(
                label="Mais",
                children=[
                    dbc.DropdownMenuItem("Home", href="http://127.0.0.1:5000/"),
                    dbc.DropdownMenuItem("Mapa", href="http://127.0.0.1:5000/interface"),
                    dbc.DropdownMenuItem("Lista", href="http://127.0.0.1:5000/lista"),
                    dbc.DropdownMenuItem("Desempenho Geral", href="http://127.0.0.1:5000/desempenho_geral"),
                    dbc.DropdownMenuItem("Histórico de Produção", href="http://127.0.0.1:5000/historico_producao"),
                    dbc.DropdownMenuItem("Produção de Energia", href="http://127.0.0.1:5000/producao_energia"),
                    dbc.DropdownMenuItem("Status em Tempo Real", href="http://127.0.0.1:5000/status_tempo_real"),
                    dbc.DropdownMenuItem("Alarmes e Notificações", href="http://127.0.0.1:5000/alertas_notificacoes"),
                    dbc.DropdownMenuItem("Login", href="http://127.0.0.1:5000/login"),
                ],
                direction='start',
                color='dark',
                id='drop-nav'
            ),

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
