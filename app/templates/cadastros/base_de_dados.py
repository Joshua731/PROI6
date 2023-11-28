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

from app.configs import db
from app.templates.cadastros.usuario import novo_usuario
from app.models.database import Database
from app.models.usuario import Usuario
from app.templates.partials.index import navbar, caminho_http, criptografar_senha
import dash_bootstrap_components as dbc

df = pd.read_csv(r'app\files\saida_atualizado.csv')

engine = create_engine('sqlite:///./database/database.db')

query = pd.read_sql(f'SELECT id_login FROM usuario WHERE nome_usuario = "{novo_usuario.nome_usuario}"', con=engine)

cad_banco = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app, url_base_pathname='/cad-db/')
cad_banco.layout = dbc.Container([
    # Navbar
    dbc.Row([
        navbar,
        dcc.Location(id='url', refresh=False),
    ]),
    # Conteúdo da página
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(sm=3),
                dbc.Col([
                    dcc.Loading([
                        dbc.Card([
                            dbc.CardHeader("Integração da fonte de dados", class_name='card-header-banco'),
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='drop-origem',
                                            placeholder='Origem dos dados',
                                            options=[
                                                {"label": 'MySQL', 'value': 'mysql'},
                                                {'label': 'SQL Server', 'value': 'sql-server'},
                                            ],
                                        )
                                    ], sm=12)
                                ]),
                                dbc.Row(id='conteudo-origem'),
                            ])
                        ], color='dark', id='card-banco')
                    ], type='cube'),
                ], sm=6),
                dbc.Col(sm=3),
            ]),
            # dbc.Row([
            #     dbc.Col(sm=2),
            #     dbc.Col([
            #         dbc.Card([
            #             dbc.CardBody([
            #                 dbc.Tabs(id='tabs-cols-db', active_tab='tab-invs', children=[
            #                     dbc.Tab(tab_id='tab-invs', label='Inversores', children=[

            #                     ]),
            #                     dbc.Tab(tab_id='tab-cm', label='Central Meteorológica', children=[
            #                         dbc.Row([
            #                             dbc.Col([
            #                                 dbc.Checkbox(
            #                                     id='check-cm',
            #                                     label='Possui Central Meteorológica? (caso não possuir, apenas ignore)',
            #                                     value=False,
            #                                 )
            #                             ], sm=12)
            #                         ]),
            #                         dbc.Row(id='row-cm')
            #                     ]),
            #                     dbc.Tab(tab_id='tab-idgt', label='IDGT', children=[
            #                         dbc.Row([
            #                             dbc.Col([
            #                                 dbc.Checkbox(
            #                                     id='check-idgt',
            #                                     label='Possui Índice de Desempenho? (caso não possuir, apenas ignore)',
            #                                     value=False,
            #                                 )
            #                             ], sm=12)
            #                         ]),
            #                         dbc.Row(id='row-idgt')
            #                     ]),
            #                     dbc.Tab(tab_id='tab-qgbt', label='QGBT', children=[
            #                         dbc.Row([
            #                             dbc.Col([
            #                                 dbc.Checkbox(
            #                                     id='check-qgbt',
            #                                     label='Possui Quadro Geral de Baixa Tensão? (caso não possuir, apenas ignore)',
            #                                     value=False,
            #                                 )
            #                             ], sm=12)
            #                         ]),
            #                         dbc.Row(id='row-qgbt')
            #                     ]),
            #                     dbc.Tab(tab_id='tab-irrad-pot', label='Irradiância x Potência', children=[
            #                         dbc.Row([
            #                             dbc.Col([
            #                                 dbc.Row([
            #                                     dbc.Card([
            #                                         dbc.CardHeader('Irradiância'),
            #                                         dbc.CardBody([
            #                                             dbc.Checkbox(
            #                                                 id='check-irrad',
            #                                                 label='Possui Irradiância? (caso não possuir, apenas ignore)',
            #                                                 value=False,
            #                                             )
            #                                         ])
            #                                     ], color='dark')
            #                                 ]),
            #                                 dbc.Row(id='row-irrad')
            #                             ], sm=6),
            #                             dbc.Col([
            #                                 dbc.Row([
            #                                     dbc.Card([
            #                                         dbc.CardHeader('Potência'),
            #                                         dbc.CardBody([
            #                                             dbc.Checkbox(
            #                                                 id='check-pot',
            #                                                 label='Possui Potência Ativa? (caso não possuir, apenas ignore)',
            #                                                 value=False,
            #                                             )
            #                                         ])
            #                                     ], color='dark')
            #                                 ]),
            #                                 dbc.Row(id='row-pot')
            #                             ], sm=6),
            #                         ])
            #                     ]),
            #                     dbc.Tab(tab_id='prod-data', label='Energia/Data', children=[
            #                         dbc.Row([
            #                             dbc.Col([
            #                                 dbc.Checkbox(
            #                                     id='check-prod',
            #                                     label='Possui Energia Injetada? (caso não possuir, apenas ignore)',
            #                                     value=False,
            #                                 ),
            #                             ])
            #                         ]),
            #                         dbc.Row(id='row-prod')
            #                     ])
            #                 ])
            #             ]),
            #         ], color='dark'),
            #     ], sm=8),
            #     dbc.Col(sm=2),
            # ]),
            # dbc.Row([
            #     dbc.Col(sm=3),
            #     dbc.Col([
            #         dbc.Card([
            #             dbc.CardBody([
            #                 dbc.Row([
            #                     dbc.Col([
            #                         dcc.Dropdown(
            #                             id='drop-estado',
            #                             options=[{'label': 'São Paulo', 'value': 'SP'}],
            #                             placeholder='Selecione o(s) estado(s) da(s) usina(s)',
            #                             multi=True,
            #                         )
            #                     ], sm=6),
            #                     dbc.Col([
            #                         dcc.Dropdown(
            #                             id='drop-cidade',
            #                             options=[{'label': cidade, 'value': cidade} for cidade in df['name']],
            #                             placeholder='Selecione a(s) cidade(s) da(s) usina(s)',
            #                             multi=True,
            #                         )
            #                     ], sm=6)
            #                 ])
            #             ])
            #         ], color='dark'),
            #     ], sm=6),
            #     dbc.Col(sm=3),
            # ])
        ], sm=12),
    ]),

], fluid=True)


@cad_banco.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname'),
)
def mostra_pagina(path):
    print(path)
    return path


@cad_banco.callback(
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
    if tipo not in ['mysql', 'sql-server']:
        return html.P('Estamos trabalhando nessa funcionalidade')


@cad_banco.callback(
    Output('url', 'pathname'),
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
def redireciona_para_colunas(tipo, base, u, senha, ip, porta, botao):
    if dash.ctx.triggered_id == 'red-cols':
        if tipo == 'sql-server':
            try:
                engine = create_engine(
                    f'mssql+pyodbc://{u}:{senha}@{ip}:{porta}/{base}?driver=ODBC+Driver+17+for+SQL+Server')
                query_teste = f'''
                        SELECT DISTINCT schema_name(schema_id)
                        FROM sys.tables;
                        '''
                pd.read_sql(query_teste, engine)

                database = Database(
                    tipo_banco=tipo,
                    base_de_dados=base,
                    usuario_db=u,
                    senha_db=criptografar_senha(senha),
                    ip=ip,
                    porta=porta,
                    usuario=novo_usuario
                )
                db.session.add(database)
                db.session.commit()
                return '/cad-cols/', html.P('OK'), 'success', 'success'
            except Exception as e:
                print(e)
                print(datetime.datetime.now())
                return '/cad-db/', html.P('Ocorreu um erro. Cheque suas informações'), 'danger', 'danger'
    raise PreventUpdate

# @cad_banco_1.callback(
#     Output('row-invs', 'children'),
#     Input('check-invs', 'value'),
# )
# def mostra_opcoes_dos_inversores(mostrar):
#     if mostrar:
#         return [
#             dbc.Col([
#                 dbc.Row([
#                     dcc.Loading([
#                         dbc.Card([
#                             dbc.CardHeader('Inversores'),
#                             dbc.CardBody([
#                                 dbc.InputGroup([
#                                     dbc.Col([
#                                         dbc.Input(id='ipt-n-invs', placeholder='Quantidade', type='number')
#                                     ], sm=4),
#                                     dbc.Col([
#                                         dbc.Input(id='ipt-tbl-base', placeholder='Tabela', type='text')
#                                     ], sm=8),
#                                 ]),
#                             ])
#                         ], color='dark'),
#                     ])
#                 ]),
#                 dbc.Row([
#                     dcc.Loading([
#                         dbc.Card([
#                             dbc.CardHeader("Colunas"),
#                             dbc.CardBody(id='cd-bd-cols-invs')
#                         ], color='dark')
#                     ], type='default')
#                 ]),
#             ], sm=12),
#         ]


# @cad_banco_1.callback(
#     Output('cd-bd-cols-invs', 'children'),
#     Input('ipt-tbl-base', 'value'),
#     Input('ipt-n-invs', 'value'),
# )
# def mostra_dropdown_das_colunas_das_tabelas(tabela, n):
#     try:
#         n_inv = []
#         id_inv = []
#         for i in range(len(n)):
#             n_inv.append(i)
#             id_inv.append(f'drop-inv-{i}')
#         query_colunas = f'''
#         select top 1 * from {tabela}
#         '''
#         df_colunas = pd.read_sql(query_colunas, create_engine(df_db['engine'])).columns
#         return [dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader(f'Inversor {i + 1}'),
#                     dbc.CardBody([
#                         dcc.Dropdown(
#                             id=f'drop-inv-{i + 1}',
#                             placeholder='Coluna respectiva',
#                             options=[
#                                 {'label': coluna, 'value': coluna}
#                                 for coluna in df_colunas
#                             ],
#                         ),
#                     ])
#                 ], color='dark')
#             ], sm=4)
#             for i in range(int(n))
#         ]),
#         ]
#     except Exception as e:
#         print(e)
#         return html.P('Tabela não encontrada')

# @cad_banco_1.callback(
#     Output('tabs-cols-db', 'active_tab'),
#     Input('check-invs', 'value'),
#     Input('red-cm', 'n_clicks'),
#     Input('ipt-n-invs', 'value'),
#     Input('ipt-tbl-base', 'value'),
#     [Input(ids, 'value') for ids in invs['id_inv']]
# )
# def redireciona_para_cm(*args):
#     print(dash.ctx.triggered_id)
#     if dash.ctx.triggered_id == 'red-cm':
#         if not args[0]:
#             return 'tab-cm'
#         else:
#             if args[1:]:
#                 return 'tab-cm'
#             else:
#                 return 'tab-invs'
#     else:
#         raise PreventUpdate
#
#
# @cad_banco_1.callback(
#     Output('row-cm', 'children'),
#     Input('check-cm', 'value')
# )
# def mostra_opcoes_cm(tem):
#     if tem:
#         return [
#             dbc.Col([
#                 dbc.Row([
#                     dbc.Input(id='ipt-tbl-cm', placeholder='Tabela da Central Meteorológica', type='text'),
#                     dbc.Card([
#                         dbc.CardHeader('Componentes'),
#                         dbc.CardBody([
#                             dbc.Row([
#                                 dbc.Col([
#                                     dbc.Checkbox(id='check-irrad-h', label='Possui Irradiação Solar Horizontal?',
#                                                  value=False)
#                                 ], sm=6),
#                                 dbc.Col([
#                                     dbc.Checkbox(id='check-irrad-i', label='Possui Irradiação Solar Inclinada?',
#                                                  value=False)
#                                 ], sm=6),
#                             ]),
#                             dbc.Row([
#                                 dbc.Col([
#                                     dbc.Checkbox(id='check-temp-amb', label='Possui Temperatura Ambiente?',
#                                                  value=False)
#                                 ], sm=6),
#                                 dbc.Col([
#                                     dbc.Checkbox(id='check-temp-plc', label='Possui Temperatura das Placas?',
#                                                  value=False)
#                                 ], sm=6),
#                             ]),
#                             dbc.Row([
#                                 dbc.Col([
#                                     dbc.Checkbox(id='check-umd-rel-ar', label='Possui Umidade Relativa do Ar?',
#                                                  value=False)
#                                 ], sm=6),
#                                 dbc.Col([
#                                     dbc.Checkbox(id='check-frq', label='Possui Frequência?', value=False)
#                                 ], sm=6),
#                                 dbc.Row([
#                                     dbc.Col([
#                                         dbc.Checkbox(id='check-dir-vt', label='Possui Direção do Vento?', value=False)
#                                     ], sm=6),
#                                     dbc.Col([
#                                         dbc.Checkbox(id='check-vel-vt', label='Possui Velocidade do Vento?',
#                                                      value=False)
#                                     ], sm=6),
#                                 ])
#                             ]),
#                         ])
#                     ], color='dark'),
#                 ]),
#                 dbc.Row(id='row-cm-comps')
#             ], sm=12),
#         ]
#
#
# @cad_banco_1.callback(
#     Output('row-cm-comps', 'children'),
#     Input('ipt-tbl-cm', 'value'),
#     Input('check-irrad-h', 'value'),
#     Input('check-irrad-i', 'value'),
#     Input('check-temp-amb', 'value'),
#     Input('check-temp-plc', 'value'),
#     Input('check-umd-rel-ar', 'value'),
#     Input('check-frq', 'value'),
#     Input('check-dir-vt', 'value'),
#     Input('check-vel-vt', 'value'),
# )
# def mostra_colunas_cm(tabela, irrad_h, irrad_i, temp_amb, temp_plc, umidade, freq, dir_vt, vel_vt):
#     query = pd.read_sql(f'SELECT TOP 1 * FROM {tabela}', df4['engine'].values[0]).columns
#     drops = []
#     componentes = [
#         'ipt-tbl-cm',
#         'check-irrad-h',
#         'check-irrad-i',
#         'check-temp-amb',
#         'check-temp-plc',
#         'check-umd-rel-ar',
#         'check-frq',
#         'check-dir-vt',
#         'check-vel-vt'
#     ]
#     lista_checks = [irrad_h, irrad_i, temp_amb, temp_plc, umidade, freq, dir_vt, vel_vt]
#     dict_comps = {
#         componentes[0]: 'Irradiação Solar Horizontal',
#         componentes[1]: 'Irradiação Solar Inclinada',
#         componentes[2]: 'Temperatura Ambiente',
#         componentes[3]: 'Temperatura das Placas',
#         componentes[4]: 'Umidade Relativa do Ar',
#         componentes[5]: 'Frequência',
#         componentes[6]: 'Direção do Vento',
#         componentes[7]: 'Velocidade do Vento',
#     }
#     for i in range(len(componentes)):
#         if lista_checks[i]:
#             drops.append(
#                 dcc.Dropdown(
#                     id=f'drop-col-{list(dict_comps.keys())[i]}',
#                     placeholder=f'Coluna para {dict_comps[componentes[i]]}',
#                     options=[{'label': q, 'value': q} for q in query]
#                 ),
#             )
#     return drops
