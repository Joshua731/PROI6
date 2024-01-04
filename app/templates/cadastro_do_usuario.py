import dash
import pandas as pd
from dash.exceptions import PreventUpdate
from sqlalchemy import create_engine

from app import app
from app.configs import db
from app.models.usuario import Usuario
from app.templates.partials.index import navbar
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

cadastro_do_usuario = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app,
                           url_base_pathname='/cadastro_usuario/')
cadastro_do_usuario.layout = dbc.Container([
    dbc.Row([
        dcc.Location(id='redirecionador'),
        dbc.Col(sm=3),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Cadastrar novo usuário'),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Input(placeholder='Digite o seu nome completo', type='text', id='input-nome')
                                ], sm=12)
                            ], class_name='rows-cadastro'),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Checkbox(
                                        id="check-empresa",
                                        label="Possui empresa?",
                                        value=False,
                                        class_name='check-cadastro'
                                    ),
                                ], sm=3),
                                dbc.Col([
                                    dbc.Input(
                                        placeholder='Digite o nome da sua empresa', type='text', id='input-empresa'
                                        , disabled=True),
                                ], sm=9)
                            ], class_name='rows-cadastro'),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Input(placeholder='Digite o seu email', type='email', id='input-email')
                                ], sm=12)
                            ], class_name='rows-cadastro'),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Input(placeholder='Digite sua senha', type='password', id='input-senha')
                                ], sm=12)
                            ], class_name='rows-cadastro'),
                            dbc.Row([
                                dbc.Col([
                                    html.Span(id='span-usuario')
                                ], sm=12)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button('Próxima etapa',
                                               id='botao-prosseguir',
                                               disabled=True,
                                               color='dark')
                                ], sm=3)
                            ])
                        ])
                    ], color='dark', class_name='cartao-usuario')
                ], sm=12)
            ])
        ], sm=6),
        dbc.Col(sm=3),
    ])
], fluid=True)


@cadastro_do_usuario.callback(
    Output('input-empresa', 'disabled'),
    Input('check-empresa', 'value')
)
def ativar_input_empresa(check):
    if check:
        return False
    else:
        return True


@cadastro_do_usuario.callback(
    Output('botao-prosseguir', 'disabled'),
    Input('input-nome', 'value'),
    Input('input-empresa', 'value'),
    Input('input-email', 'value'),
    Input('input-senha', 'value'),
)
def habilitar_botao_proxima_etapa(nome, empresa, email, senha):
    if nome and empresa and email and senha:
        return False


@cadastro_do_usuario.callback(
    Output('redirecionador', 'pathname'),
    Output('span-usuario', 'children'),
    Input('input-nome', 'value'),
    Input('input-empresa', 'value'),
    Input('input-email', 'value'),
    Input('input-senha', 'value'),
    Input('check-empresa', 'value'),
    Input('botao-prosseguir', 'n_clicks')
)
def redirecionar_para_cadastro_do_banco(nome, empresa, email, senha, check, botao):
    if nome and email and senha and dash.ctx.triggered_id == 'botao-prosseguir':
        engine = create_engine('sqlite:///database/database.db')
        df = pd.read_sql(f"""SELECT nome_usuario 
                             FROM usuario 
                             WHERE email_login = '{email}'
                             AND senha_login = '{senha}'
                             AND nome_usuario = '{nome}'
                             """, engine)
        if df.empty:
            novo_usuario = Usuario(
                nome_usuario=nome,
                nome_empresa=empresa if check else 'sem empresa',
                email_login=email,
                senha_login=senha
            )
            db.session.add(novo_usuario)
            db.session.commit()
            return '/home/', 'Usuário criado com sucesso!'
        else:
            return None, 'Usuário já existente!'
    raise PreventUpdate

