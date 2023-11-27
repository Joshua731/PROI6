import datetime

import dash
import pandas as pd
import pyodbc
import requests
import sqlalchemy
from dash.exceptions import PreventUpdate
from sqlalchemy import create_engine

from app import app
from dash import Dash, dcc, html, Input, Output
from app.templates.partials.index import navbar, caminho_http
import dash_bootstrap_components as dbc

estados = [
    {'label': 'Acre', 'value': 'AC'},
    {'label': 'Alagoas', 'value': 'AL'},
    {'label': 'Amapá', 'value': 'AP'},
    {'label': 'Amazonas', 'value': 'AM'},
    {'label': 'Bahia', 'value': 'BA'},
    {'label': 'Ceará', 'value': 'CE'},
    {'label': 'Distrito Federal', 'value': 'DF'},
    {'label': 'Espírito Santo', 'value': 'ES'},
    {'label': 'Goiás', 'value': 'GO'},
    {'label': 'Maranhão', 'value': 'MA'},
    {'label': 'Mato Grosso', 'value': 'MT'},
    {'label': 'Mato Grosso do Sul', 'value': 'MS'},
    {'label': 'Minas Gerais', 'value': 'MG'},
    {'label': 'Pará', 'value': 'PA'},
    {'label': 'Paraíba', 'value': 'PB'},
    {'label': 'Paraná', 'value': 'PR'},
    {'label': 'Pernambuco', 'value': 'PE'},
    {'label': 'Piauí', 'value': 'PI'},
    {'label': 'Rio de Janeiro', 'value': 'RJ'},
    {'label': 'Rio Grande do Norte', 'value': 'RN'},
    {'label': 'Rio Grande do Sul', 'value': 'RS'},
    {'label': 'Rondônia', 'value': 'RO'},
    {'label': 'Roraima', 'value': 'RR'},
    {'label': 'Santa Catarina', 'value': 'SC'},
    {'label': 'São Paulo', 'value': 'SP'},
    {'label': 'Sergipe', 'value': 'SE'},
    {'label': 'Tocantins', 'value': 'TO'}
]

variaveis_globais = {}

df_variaveis = pd.DataFrame({'quantidade_de_inversores': [4]})
df_variaveis.to_excel(r'app\templates\formularios\temp.xlsx', index=False)
df = pd.read_csv(r'app\files\saida_atualizado.csv')

cad_banco_1 = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app, url_base_pathname='/cadastro-1/')
cad_banco_1.layout = dbc.Container([
    # Navbar
    dbc.Row([
        navbar,
        dcc.Location(id='url', refresh=False),
    ]),
    # Conteúdo da página
    dbc.Row([
        dbc.Col([
            dbc.Tabs(id='tabs-cad', active_tab='cad-usuario', children=[
                dbc.Tab(label='Usuário', tab_id='cad-usuario', children=[
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
                                        dcc.Input(type="text", id="company-input",
                                                  placeholder="Entre com a sua Empresa",
                                                  className="form-control"),
                                        html.Label('Email'),
                                        dcc.Input(type="email", id="email-input", placeholder="Entre com o seu Email",
                                                  className="form-control"),
                                        html.Label("Senha"),
                                        dcc.Input(type="password", id="password-input",
                                                  placeholder="Entre com a sua Senha",
                                                  className="form-control"),

                                        html.Div(id="signup-message", className="mt-3"),
                                    ]),
                                ], color='dark', className='crd'),
                            ]),
                        ], sm=6),
                        dbc.Col([], sm=3),
                    ], className="mt-4"),
                ]),
                dbc.Tab(label='Banco', tab_id='cad-db', children=[
                    dbc.Row([
                        dbc.Col(sm=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Integração da fonte de dados", class_name='card-header-banco'),
                                dbc.CardBody([
                                    dbc.Row([
                                        dcc.Dropdown(
                                            id='drop-origem',
                                            placeholder='Origem dos dados',
                                            options=[
                                                {"label": 'MySQL', 'value': 'mysql'},
                                                {'label': 'SQL Server', 'value': 'sql-server'},
                                            ],
                                        )
                                    ]),
                                    dbc.Row(id='conteudo-origem'),
                                ])
                            ], color='dark', id='card-banco')
                        ], sm=6),
                        dbc.Col(sm=3),
                    ])
                ]),
                dbc.Tab(tab_id='sel-cols', label='Colunas', children=[
                    dbc.Row([
                        dbc.Col(sm=2),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Tabs(id='tabs-cols-db', active_tab='tab-invs', children=[
                                        dbc.Tab(tab_id='tab-invs', label='Inversores', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Row([
                                                        dbc.Checkbox(
                                                            id='check-invs',
                                                            label='Possui Inversores? (caso não possuir, apenas ignore)',
                                                            value=False,
                                                        )
                                                    ]),
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dbc.Button('Próximo', color='dark', id='red-cm')
                                                        ], sm=2)
                                                    ])
                                                ], sm=12)
                                            ]),
                                            dbc.Row(id='row-invs'),
                                        ]),
                                        dbc.Tab(tab_id='tab-cm', label='Central Meteorológica', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checkbox(
                                                        id='check-cm',
                                                        label='Possui Central Meteorológica? (caso não possuir, apenas ignore)',
                                                        value=False,
                                                    )
                                                ], sm=12)
                                            ]),
                                            dbc.Row(id='row-cm')
                                        ]),
                                        dbc.Tab(tab_id='tab-idgt', label='IDGT', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checkbox(
                                                        id='check-idgt',
                                                        label='Possui Índice de Desempenho? (caso não possuir, apenas ignore)',
                                                        value=False,
                                                    )
                                                ], sm=12)
                                            ]),
                                            dbc.Row(id='row-idgt')
                                        ]),
                                        dbc.Tab(tab_id='tab-qgbt', label='QGBT', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checkbox(
                                                        id='check-qgbt',
                                                        label='Possui Quadro Geral de Baixa Tensão? (caso não possuir, apenas ignore)',
                                                        value=False,
                                                    )
                                                ], sm=12)
                                            ]),
                                            dbc.Row(id='row-qgbt')
                                        ]),
                                        dbc.Tab(tab_id='tab-irrad-pot', label='Irradiância x Potência', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Row([
                                                        dbc.Card([
                                                            dbc.CardHeader('Irradiância'),
                                                            dbc.CardBody([
                                                                dbc.Checkbox(
                                                                    id='check-irrad',
                                                                    label='Possui Irradiância? (caso não possuir, apenas ignore)',
                                                                    value=False,
                                                                )
                                                            ])
                                                        ], color='dark')
                                                    ]),
                                                    dbc.Row(id='row-irrad')
                                                ], sm=6),
                                                dbc.Col([
                                                    dbc.Row([
                                                        dbc.Card([
                                                            dbc.CardHeader('Potência'),
                                                            dbc.CardBody([
                                                                dbc.Checkbox(
                                                                    id='check-pot',
                                                                    label='Possui Potência Ativa? (caso não possuir, apenas ignore)',
                                                                    value=False,
                                                                )
                                                            ])
                                                        ], color='dark')
                                                    ]),
                                                    dbc.Row(id='row-pot')
                                                ], sm=6),
                                            ])
                                        ]),
                                        dbc.Tab(tab_id='prod-data', label='Energia/Data', children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checkbox(
                                                        id='check-prod',
                                                        label='Possui Energia Injetada? (caso não possuir, apenas ignore)',
                                                        value=False,
                                                    ),
                                                ])
                                            ]),
                                            dbc.Row(id='row-prod')
                                        ])
                                    ])
                                ]),
                            ], color='dark'),
                        ], sm=8),
                        dbc.Col(sm=2),
                    ]),
                ]),
                dbc.Tab(tab_id='tab-usinas', label='Usinas', children=[
                    dbc.Row([
                        dbc.Col(sm=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='drop-estado',
                                                options=[{'label': 'São Paulo', 'value': 'SP'}],
                                                placeholder='Selecione o(s) estado(s) da(s) usina(s)',
                                                multi=True,
                                            )
                                        ], sm=6),
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='drop-cidade',
                                                options=[{'label': cidade, 'value': cidade} for cidade in df['name']],
                                                placeholder='Selecione a(s) cidade(s) da(s) usina(s)',
                                                multi=True,
                                            )
                                        ], sm=6)
                                    ])
                                ])
                            ], color='dark'),
                        ], sm=6),
                        dbc.Col(sm=3),
                    ])

                ])
            ]),
        ], sm=12),
    ]),

], fluid=True)


@cad_banco_1.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname'),
)
def mostra_pagina(path):
    print(path)
    return path


# @cad_banco_1.callback(
#

# )
# def redireciona(db, usuario, senha, IP, porta, n_cliques):
#     if dash.ctx.triggered_id == 'red-pt-2':
#         url = f'http://{caminho_http}/cadastro'  # URL da rota do Flask
#         data = {'db': db, 'usuario_db': usuario, 'senha_db': senha, 'IP_db': IP, 'porta_db': porta}
#
#         response = requests.post(url, data=data)  # Envia os dados para o Flask
#         return response.text  # Exibe a mensagem de resposta do Flask na interface Dash


@cad_banco_1.callback(
    Output("conteudo-origem", "children"),
    Input('drop-origem', 'value')
)
def mostrar_dados_pelo_tipo_de_cadastro(tipo):
    if tipo is None:
        raise PreventUpdate
    if tipo in ['mysql', 'sql-server']:
        return dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-db', placeholder='Nome da base de dados',
                                  type='text')
                    ])
                ], sm=12),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-usuario', placeholder='Usuário', type='text')
                    ])
                ], sm=6),
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-senha', placeholder='Senha', type='password')
                    ])
                ], sm=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-IP', placeholder='Endereço IP', type='text')
                    ])
                ], sm=9),
                dbc.Col([
                    dbc.Row([
                        dbc.Input(id='input-porta', placeholder='Porta', type='number')
                    ])
                ], sm=3)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Próximo', id='red-cols', color='dark')
                ], sm=2)
            ]),
            dbc.Row(id='status-banco'),

        ], sm=12)
    if not tipo in ['mysql', 'sql-server']:
        return html.P('Estamos trabalhando nessa funcionalidade')


@cad_banco_1.callback(
    Output('tabs-cad', 'active_tab'),
    Output('status-banco', 'children'),
    Output('card-banco', 'color'),
    Output('red-cols', 'color'),
    Input('drop-origem', 'value'),
    Input('input-db', 'value'),
    Input('input-usuario', 'value'),
    Input('input-senha', 'value'),
    Input('input-IP', 'value'),
    Input('input-porta', 'value'),
    Input('red-cols', 'n_clicks'),
)
def redireciona_para_colunas(tipo, base, usuario, senha, ip, porta, botao):
    if dash.ctx.triggered_id == 'red-cols':
        if tipo == 'sql-server':
            try:
                engine = create_engine(
                    f'mssql+pyodbc://{usuario}:{senha}@{ip}:{porta}/{base}?driver=ODBC+Driver+17+for+SQL+Server')
                df_variaveis[
                    'engine'] = f'mssql+pyodbc://{usuario}:{senha}@{ip}:{porta}/{base}?driver=ODBC+Driver+17+for+SQL+Server'
                df_variaveis['tipo'] = tipo
                df_variaveis['db'] = base
                df_variaveis['usuario'] = usuario
                df_variaveis['senha'] = senha
                df_variaveis['ip'] = ip
                df_variaveis['porta'] = porta
                df_variaveis.to_excel(r'app\templates\formularios\temp.xlsx', index=False)
                query_teste = f'''
                        SELECT DISTINCT schema_name(schema_id)
                        FROM sys.tables;
                        '''
                pd.read_sql(query_teste, engine)
                return 'sel-cols', html.P('OK'), 'success', 'success'
            except Exception as e:
                print(e)
                print(datetime.datetime.now())
                return 'cad-db', html.P('Ocorreu um erro. Cheque suas informações'), 'danger', 'danger'
    raise PreventUpdate


@cad_banco_1.callback(
    Output('row-invs', 'children'),
    Input('check-invs', 'value'),
)
def mostra_opcoes_dos_inversores(mostrar):
    if mostrar:
        return [
            dbc.Col([
                dbc.Row([
                    dcc.Loading([
                        dbc.Card([
                            dbc.CardHeader('Inversores'),
                            dbc.CardBody([
                                dbc.InputGroup([
                                    dbc.Col([
                                        dbc.Input(id='ipt-n-invs', placeholder='Quantidade', type='number')
                                    ], sm=4),
                                    dbc.Col([
                                        dbc.Input(id='ipt-tbl-base', placeholder='Tabela', type='text')
                                    ], sm=8),
                                ]),
                            ])
                        ], color='dark'),
                    ])
                ]),
                dbc.Row([
                    dcc.Loading([
                        dbc.Card([
                            dbc.CardHeader("Colunas"),
                            dbc.CardBody(id='cd-bd-cols-invs')
                        ], color='dark')
                    ], type='default')
                ]),
            ], sm=12),
        ]


@cad_banco_1.callback(
    Output('cd-bd-cols-invs', 'children'),
    Input('ipt-tbl-base', 'value'),
    Input('ipt-n-invs', 'value'),
)
def mostra_dropdown_das_colunas_das_tabelas(tabela, n):
    try:
        df2 = pd.read_excel(r'app\templates\formularios\temp.xlsx')
        df2['tabela_dos_inversores'] = tabela
        df2['quantidade_de_inversores'] = n
        df2.to_excel(r'app\templates\formularios\temp.xlsx', index=False)
        query_colunas = f'''
        select * from {tabela}
        '''
        df_colunas = pd.read_sql(query_colunas, create_engine(str(df2['engine'].values[0]))).columns
        return [dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(f'Inversor {i + 1}'),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id=f'drop-inv-{i}',
                            placeholder='Coluna respectiva',
                            options=[
                                {'label': coluna, 'value': coluna}
                                for coluna in df_colunas],
                        ),
                    ])
                ], color='dark')
            ], sm=4)
            for i in range(int(n))
        ]),
        ]
    except Exception as e:
        print(e)
        return html.P('Tabela não encontrada')


csv = pd.read_excel(r'app\templates\formularios\temp.xlsx')


@cad_banco_1.callback(
    Output('tabs-cols-db', 'active_tab'),
    Input('red-cm', 'n_clicks'),
    Input('ipt-n-invs', 'value'),
    Input('ipt-tbl-base', 'value'),
    [Input(f'drop-inv-{i}', 'value') for i in range(int(csv['quantidade_de_inversores']))]
)
def redireciona_para_cm(*args):
    df3 = pd.read_excel(r'app\templates\formularios\temp.xlsx')
    if dash.ctx.triggered_id == 'red-cm' and args[1] and args[2] and args[3:]:
        for i in range(3, int(df3['quantidade_de_inversores'])):
            df3['colunas_dos_inversores'] = args[i]
        return 'tab-cm'

@cad_banco_1.callback(
    Output('row-cm', 'children'),
    Input('check-cm', 'value')
)
def mostra_opcoes_cm(tem):
    if tem:
        return dbc.Col([
            dbc.Row([
                dbc.Checkbox(id='check-irrad-h', label='Possui Irradiação Solar Horizontal?', value=False)
            ]),
            dbc.Row([
                dbc.Checkbox(id='check-irrad-i', label='Possui Irradiação Solar Inclinada?', value=False)
            ]),
            dbc.Row([
                dbc.Checkbox(id='check-temp-amb', label='Possui Temperatura Ambiente?', value=False)
            ]),
            dbc.Row([
                dbc.Checkbox(id='check-temp-plc', label='Possui Temperatura das Placas?', value=False)
            ]),
            dbc.Row([
                dbc.Checkbox(id='check-umd-rel-ar', label='Possui Umidade Relativa do Ar?', value=False)
            ]),
        ], sm=12)
