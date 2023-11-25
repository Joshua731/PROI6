import json

import dash
import dash_auth
import pandas as pd
import requests
from sqlalchemy import create_engine

from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from app.templates.partials.index import navbar, get_local_ip

custom_css = {
    'text-light': {'color': 'white'},
    'bg-light': {'background-color': 'white'},
    '.body': {'background-color': '#A9A9A9'},
    'font': 'dict(color='  # cccccc)',
}

login_page = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname="/login/")
login_page.layout = dbc.Container(
    [
        # Navbar
        navbar,
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col([], sm=3),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Login", className="card-title"),
                            html.Label("Usuario"),
                            dcc.Input(type="text", id="username-input", placeholder="Entre com seu Usuario",
                                      className="form-control"),
                            html.Label("Senha"),
                            dcc.Input(type="password", id="password-input", placeholder="Entre com a sua Senha",
                                      className="form-control"),
                            dbc.Button("Login", id="login-button", className="btn btn-block", n_clicks=0, outline=True,
                                       color='light', href=f'http://{get_local_ip()}:5000/index'),
                            html.Div(id="login-message", className="mt-3"),
                        ])
                    ], color='dark', className='crd'),
                ]),
            ], sm=6),
            dbc.Col([], sm=3),
        ], className="mt-4"),
    ],
    fluid=True,
)


# Callback to handle login logic
@login_page.callback(
    Output("login-message", "children"),
    Input("login-button", "n_clicks"),
    Input("username-input", "value"),
    Input("password-input", "value"),
)
def handle_login(n_clicks, usuario, senha):
    if dash.ctx.triggered_id == 'login-button':
        url = f'http://{get_local_ip()}:5000/login'  # URL da rota do Flask
        data = {'usuario': usuario, 'senha': senha}

        response = requests.post(url, data=data)  # Envia os dados para o Flask

        if response.status_code == 200:  # Assumindo que o código 200 indica sucesso
            return ''  # Redireciona para a página 'index'

        return response.text




@login_page.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path
