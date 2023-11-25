import json
import socket

import dash_auth
from sqlalchemy import create_engine

from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np


def get_local_ip():
    try:
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    except socket.error as e:
        return f"Ocorreu um erro ao tentar obter o IP interno: {e}"


caminho_http = f'http://{get_local_ip()}:5000'

navbar = html.Div([
    dbc.NavbarSimple(
        brand="Bem-vindo a Dashua",
        brand_href=f"{caminho_http}:5001/",
        color="dark",
        dark=True,
        children=[
            dbc.DropdownMenu(
                label="Mais",
                children=[
                    dbc.DropdownMenuItem("Home", href=f"{caminho_http}/"),
                    # dbc.DropdownMenuItem("Login", href=f"{caminho_http}/login"),
                    dbc.DropdownMenuItem("Formulario", href=f"{caminho_http}/formulario_db"),
                    dbc.DropdownMenuItem("Mapa", href=f"{caminho_http}/interface"),
                    dbc.DropdownMenuItem("Lista", href=f"{caminho_http}/lista"),
                    dbc.DropdownMenuItem("Desempenho Geral", href=f"{caminho_http}/desempenho_geral"),
                    dbc.DropdownMenuItem("Histórico de Produção", href=f"{caminho_http}/historico_producao"),
                    dbc.DropdownMenuItem("Produção de Energia", href=f"{caminho_http}/producao_energia"),
                    dbc.DropdownMenuItem("Status em Tempo Real", href=f"{caminho_http}/status_tempo_real"),
                    dbc.DropdownMenuItem("Alarmes e Notificações", href=f"{caminho_http}/alertas_notificacoes"),
                ],
                direction='start',
                color='dark',
                id='drop-nav'
            ),

        ],
        id='logo-usina'
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
