import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc, Input, Output
from sqlalchemy import create_engine

from app.configs import db
from app.models.inversores import Inversor
from app.templates.cadastros.base_de_dados import nova_database

from app import app
from app.templates.cadastros.base_de_dados import string_engine
from app.templates.partials.index import caminho_http

engine = create_engine('sqlite:///./database/database.db')

user = nova_database.usuario_db
tipo = nova_database.tipo_banco
ip = nova_database.ip
porta = nova_database.porta
senha = nova_database.senha_db
base = nova_database.base_de_dados

inversores = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SOLAR],
    server=app,
    url_base_pathname='/cadastro/colunas/inversores/')

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
                            html.Link('Prosseguir', id='next-etp-1')
                        ], sm=2)
                    ])
                ]),
                dbc.CardFooter(dbc.Button('Ir para a próxima página', disabled=True, id='btn-red-cm'))
            ], color='dark')
        ])
    ]),
], fluid=True)

tabela_inversores = dbc.Col(
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
                        dbc.Input(id='input-tbl', placeholder='Digite a tabela que contém os inversores')
                    ], sm=10
                )
            ]
        ),
        dbc.Row(
            [
                html.H6(id='tabela-existe')
            ]
        ),
        html.Link('Prosseguir', id='next-etp-2'),
        dbc.Row(id='row-cols')
    ], sm=12
),


@inversores.callback(
    Output('row-qtd', 'children'),
    Input('check-invs', 'value'),
    Input('next-etp-1', 'n_clicks'),
    Input('btn-red-cm', 'n_clicks'),
)
def mostrar_aba_da_quantidade_dos_inversores(tem_inv, btn_etp, btn_red):
    if dash.ctx.triggered_id == "next-etp-1" and tem_inv:
        return tabela_inversores
    if dash.ctx.triggered_id == 'btn-red-cm' and not tem_inv:
        novo_inversor = Inversor(tabela=None, numero=None, correspondente=None, database_id=nova_database)
        db.session.add(novo_inversor)
        return html.A('Central Meteorológica', href=f'{caminho_http}/cadastro/colunas/cm')

    @inversores.callback(
        Output('row-cols', 'children'),
        Input('input-tbl', 'value'),
        Input('ipt-n-invs', 'value'),
    )
    def mostrar_aba_da_selecao_de_colunas(input, quant):
        @inversores.callback(
            Output('url', 'pathname'),
            Input('red-cm', 'n_clicks'),
            [Input(f'drop-inv-{i + 1}', 'value') for i in range(int(quant))]
        )
        def mostrar_aba_de_selecionar_tabela(*args):
            df_check = pd.read_sql(F'SELECT * FROM {input}', con=engine)
            if dash.ctx.triggered_id == 'red-cm' and args[1:] and tem_inv and quant and not df_check.empty:
                for i in range(len(args[1:])):
                    novo_inversor = Inversor(
                        tabela=input,
                        numero=i + 1,
                        correspondente=args[i + 1],
                        database_id=nova_database)
                    db.session.add(novo_inversor)
                    db.session.commit()
                    return '/cadastro/colunas/cm'
            if dash.ctx.triggered_id == 'red-cm' and not args[1:]:
                return None

        engine = create_engine(
            f'mssql+pyodbc://{user}:{senha}@{ip}:{porta}/{base}?driver=ODBC+Driver+17+for+SQL+Server')

        colunas_db = pd.read_sql(f'SELECT * FROM {input}', con=engine).columns
        if not colunas_db.empty and quant and tem_inv:
            colunas_util = pd.read_sql(f'SELECT * FROM {input}', con=engine).columns
            return mostrar_dropdowns_das_colunas_dos_inversores(quant, colunas_util)


def mostrar_dropdowns_das_colunas_dos_inversores(n, df):
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
                            for col in df
                        ],
                    ),
                ])
            ], color='dark')
        ], sm=4)
        for i in range(int(n))
    ]


