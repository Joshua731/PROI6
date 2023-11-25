import json

import dash

from app import app
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

from app.templates import index
from app.templates.partials.index import navbar, get_local_ip

custom_css = {
    'text-light': {'color': 'white'},
    'bg-light': {'background-color': 'white'},
    '.body': {'background-color': '#A9A9A9'},
    'font': 'dict(color='  # cccccc)',
}

cadastro = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname="/cadastro/")
cadastro.layout = dbc.Container(
    [
        # Navbar
        navbar,
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col([], sm=3),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardHeader('Cadastro do Usuário', class_name='card-title'),
                        dbc.CardBody([
                            html.Label("Nome Completo"),
                            dcc.Input(type="text", id="username-input", placeholder="Entre com seu Usuario",
                                      className="form-control"),
                            html.Label('Empresa'),
                            dcc.Input(type="text", id="company-input", placeholder="Entre com a sua Empresa",
                                      className="form-control"),
                            html.Label('Email'),
                            dcc.Input(type="email", id="email-input", placeholder="Entre com o seu Email",
                                      className="form-control"),
                            html.Label("Senha"),
                            dcc.Input(type="password", id="password-input", placeholder="Entre com a sua Senha",
                                      className="form-control"),

                            html.Div(id="signup-message", className="mt-3"),
                        ]),
                        dbc.CardFooter(html.A('Concluir', id='redirecionar-home'))
                    ], color='dark', className='crd'),
                ]),
            ], sm=6),
            dbc.Col([], sm=3),
        ], className="mt-4"),
    ],
    fluid=True,
)
import requests


@cadastro.callback(
    # Output('signup-message', 'children'),
    Output('redirecionar-home', 'href'),
    [Input('redirecionar-home', 'n_clicks')],
    [State('username-input', 'value'),
     State('company-input', 'value'),
     State('email-input', 'value'),
     State('password-input', 'value')]
)
def cadastrar_usuario(n_clicks, nome, empresa, email, senha):
    if dash.ctx.triggered_id == 'redirecionar-home':
        url = f'http://{get_local_ip()}:5000/cadastro'  # URL da rota do Flask
        data = {'username-input': nome, 'company-input': empresa, 'email-input': email, 'password-input': senha}

        response = requests.post(url, data=data)  # Envia os dados para o Flask
        return response.text  # Exibe a mensagem de resposta do Flask na interface Dash


@cadastro.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path