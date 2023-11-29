import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc, Input, Output
from sqlalchemy import create_engine

from app.configs import db
from app.models.temp.cols_qtd import Quantidade
from app.templates.cadastros.base_de_dados import nova_database

from app import app

q = Quantidade(quantidade='teste', tabela='teste')
engine = create_engine('sqlite:///./database/database.db')

inversores = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SOLAR],
    server=app,
    url_base_pathname='/cadastro/colunas/inversores/check/')

tabelas = pd.read_sql(f'SELECT lista_colunas FROM colunas_database', con=engine).values

inversores.layout = dbc.Container([
    dcc.Location(id='url'),
    dbc.Row([
        dbc.Row([
            dbc.Card([
                dbc.CardHeader('Verificar existência dos inversores'),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Checkbox(
                            id='check-invs',
                            label='Possui inversor? (Clique em prosseguir, caso contrário)',
                            value=False
                        )
                    ]),
                    dbc.Row(id='row-qtd'),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button('Prosseguir', id='red-cm', color='dark')
                        ], sm=2)
                    ])
                ])
            ], color='dark')
        ])
    ]),
], fluid=True)

tabela_inversores = dbc.Row([
    dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Input(
                                id='ipt-n-invs',
                                placeholder='Quantidade',
                                type='number')
                        ], sm=2
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id='drop-tbl',
                                placeholder='selecione a tabela',
                                options=[{'label': tabela, 'value': tabela} for tabela in tabelas]
                            )
                        ], sm=10
                    )
                ]
            ),
            dbc.Row(
                [
                    html.H6(id='tabela-existe')
                ]
            ),
            dbc.Row(id='row-cols')
        ], sm=12
    ),
])


@inversores.callback(
    Output('row-qtd', 'children'),
    Output('url', 'pathname'),
    Input('check-invs', 'value'),
    Input('red-cm-quant', 'n_clicks'),
)
def mostrar_aba_da_quantidade_dos_inversores(tem_inv, bt_red):
    if dash.ctx.triggered_id == "red-cm-quant" and tem_inv:
        return tabela_inversores, None
    if dash.ctx.triggered_id == 'red-cm-quant' and not tem_inv:
        return None, '/cadastro/colunas/cm'


tabelas = pd.read_sql(f'SELECT lista_colunas FROM colunas_database', con=engine).values


@inversores.callback(
    Output('row-cols', 'children'),
    Input('drop-tbl', 'value'),
    Input('ipt-n-invs', 'value'),
)
def mostrar_aba_da_selecao_de_colunas(drop, quant):
    global q
    consulta = pd.read_sql('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS',
                           con=create_engine(nova_database.string_engine))['TABLE_NAME'].unique()

    if drop in consulta.values:
        colunas = pd.read_sql(f'SELECT * FROM {drop}', con=create_engine(nova_database.string_engine)).columns
        qtd = Quantidade(quantidade=quant, tabela=drop, colunas_database_id=nova_database)
        db.session.add(qtd)
        db.session.commit()
        q = qtd
        return [
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(f'Inversor {i + 1}'),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id=f'drop-inv-{i + 1}',
                            placeholder='Coluna respectiva',
                            options=[
                                {'label': col, 'value': col}
                                for col in colunas
                            ],
                        ),
                    ])
                ], color='dark')
            ], sm=4)
            for i in range(int(quant))
        ]


quantidade = pd.read_sql(f'SELECT quantidade FROM quantidade WHERE tabela = "{q.tabela}"', con=engine)
print(quantidade)
quant_if = quantidade['quantidade'].values if not quantidade.empty else 1


@inversores.callback(
    Output('url', 'pathname'),
    Input('red-cm', 'n_clicks'),
    Input('ipt-n-invs', 'value'),
    Input('drop-tbl', 'value'),
    [Input(f'drop-inv-{i}', 'value') for i in range(int(quant_if))]
)
def mostrar_aba_de_selecionar_tabela(*args):
    if dash.ctx.triggered_id == 'red-cm' and args[1:]:
        return '/cadastro/colunas/cm'
    if dash.ctx.triggered_id == 'red-cm' and not args[1:]:
        return None
