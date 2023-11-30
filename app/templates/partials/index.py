import json
import socket

import bcrypt
import dash_auth
from sqlalchemy import create_engine

from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np


def criptografar_senha(senha):
    # Gere um salt (um valor aleatório único)
    salt = bcrypt.gensalt()

    # Hash da senha usando o salt
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)

    return senha_hash


def verificar_senha(senha, senha_hash):
    # Verifique se a senha fornecida corresponde ao hash
    return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)


def get_local_ip():
    try:
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    except socket.error as e:
        return f"Ocorreu um erro ao tentar obter o IP interno: {e}"


caminho_http = f'http://{get_local_ip()}:5002'

navbar = html.Div([
    dbc.NavbarSimple(
        brand="Bem-vindo a Dashua",
        brand_href=f"{caminho_http}/",
        color="dark",
        dark=True,
        children=[
            dbc.DropdownMenu(
                label="Mais",
                children=[
                    dbc.DropdownMenuItem("Home", href=f"{caminho_http}/"),
                    # dbc.DropdownMenuItem("Login", href=f"{caminho_http}/login"),
                    # dbc.DropdownMenuItem("Formulario", href=f"{caminho_http}/formulario_db"),
                    dbc.DropdownMenuItem("Overview", href=f"{caminho_http}/overview"),
                    # dbc.DropdownMenuItem("Lista", href=f"{caminho_http}/lista"),
                    # dbc.DropdownMenuItem("Desempenho Geral", href=f"{caminho_http}/desempenho_geral"),
                    dbc.DropdownMenuItem("Histórico de Produção", href=f"{caminho_http}/historico_producao"),
                    # dbc.DropdownMenuItem("Produção de Energia", href=f"{caminho_http}/producao_energia"),
                    # dbc.DropdownMenuItem("Status em Tempo Real", href=f"{caminho_http}/status_tempo_real"),
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


def basic_auth_wrapper(basic_auth, func):
    """Updated auth wrapper to work on all pages rather than just index"""

    def wrap(*args, **kwargs):
        if basic_auth.is_authorized() or 'inicial' in func.__module__:
            return func(*args, **kwargs)
        # if basic_auth.is_authorized() and 'inicial' in func.__module__:
        #     return func(*args, **kwargs)
        return basic_auth.login_request()

    return wrap
