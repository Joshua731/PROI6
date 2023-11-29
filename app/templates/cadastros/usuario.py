import json

import dash
import pandas as pd
from sqlalchemy import exists, create_engine

from app import app
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

from app.models.usuario import Usuario
from app.templates.partials.index import navbar, criptografar_senha
from app.configs import db

novo_usuario = Usuario(nome_usuario='teste')

engine = create_engine('sqlite:///./database/database.db')

cad_usuario = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR],
                   url_base_pathname="/cadastro/usuario/")
cad_usuario.layout = dbc.Container(
    [
        # Navbar
        navbar,
        dcc.Location(id='url'),
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
                        dbc.CardFooter(html.A('Concluir', id='redi-home'))
                    ], color='dark', className='crd'),
                ]),
            ], sm=6),
            dbc.Col([], sm=3),
        ], className="mt-4"),
    ],
    fluid=True,
)
import requests


@cad_usuario.callback(
    Output('url', 'pathname'),
    [Input('redi-home', 'n_clicks')],
    [State('username-input', 'value'),
     State('company-input', 'value'),
     State('email-input', 'value'),
     State('password-input', 'value')]
)
def cadastrar_usuario(n_clicks, nome, empresa, email, senha):
    global novo_usuario
    if dash.ctx.triggered_id == 'redi-home' and nome and empresa and email and senha:
        df = pd.read_sql(f'SELECT nome_usuario, senha_login FROM usuario WHERE email_login = "{email}"', con=engine)
        if df.empty:
            novo_usuario = Usuario(
                nome_usuario=nome,
                nome_empresa=empresa,
                email_login=email,
                senha_login=criptografar_senha(senha)
            )
            db.session.add(novo_usuario)
            db.session.commit()
            return '/cadastro/database'
        else:
            return '/cadastro/usuario'


@cad_usuario.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path
