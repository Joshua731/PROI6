import json

import dash_auth
from dash.exceptions import PreventUpdate
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np

from app.configs import usuario, senha, ip, porta, base
from app.templates.partials.index import navbar
from screeninfo import get_monitors
from sqlalchemy import create_engine

import datetime

engine = create_engine('sqlite:///./database/database.db')

orindiuva = create_engine('sqlite:///F:/PROI6/database/orindiuva.db')
elias = create_engine('sqlite:///F:/PROI6/database/elias_fausto.db')
monte = create_engine('sqlite:///F:/PROI6/database/monte_alto.db')
paraguacu = create_engine('sqlite:///F:/PROI6/database/paraguacu.db')
rancharia = create_engine('sqlite:///F:/PROI6/database/rancharia.db')
suzano = create_engine('sqlite:///F:/PROI6/database/suzano.db')
tropeiros = create_engine('sqlite:///F:/PROI6/database/tropeiros.db')
databases = {
    'db': [],
    'banco': [],
    'usuario': [],
    'senha': [],
    'endereço': [],
    'porta': []
}

dados = pd.read_sql('SELECT * FROM bancos', con=engine)

for i in range(len(dados)):
    databases['db'].append(dados['base'].values[i])
    databases['banco'].append(dados['tipo'].values[i])
    databases['usuario'].append(dados['user'].values[i])
    databases['senha'].append(dados['pwd'].values[i])
    databases['endereço'].append(dados['ip'].values[i])
    databases['porta'].append(dados['port'].values[i])

# Supondo que você já tenha importado as bibliotecas necessárias e tenha a variável 'databases' preenchida com os dados

db = databases
engines = {}

for i in range(len(dados)):
    connection_str = f'mssql+pyodbc://{db["usuario"][i]}:{db["senha"][i]}@{db["endereço"][i]}/{db["db"][i]}?driver=ODBC+Driver+17+for+SQL+Server'
    db_name = db['db'][i]

    # Verifica se a chave já existe no dicionário engines
    if db_name not in engines:
        engines[db_name] = []  # Inicializa a lista vazia para essa chave se não existir

    # Cria a conexão e adiciona à lista correspondente no dicionário
    connection = create_engine(connection_str)
    engines[db_name].append(connection)

print(databases)
print(engines)


# Simulação de dados diários de produção de energia
def daily_energy_simulation(day_hour):
    if day_hour < 6 or day_hour >= 24:
        return 0
    else:
        return np.sin(np.pi * (day_hour - 6) / 18) ** 2


# Simulação de produção de energia diária por hora
daily_energy = [daily_energy_simulation(i) for i in range(24)]


# Simulação de dados mensais de produção de energia
def monthly_energy_simulation(month_day):
    return sum([daily_energy_simulation(i) for i in range(24)])


# Simulação de produção de energia mensal por dia
monthly_energy = [monthly_energy_simulation(i) for i in range(1, 32)]


# Simulação de dados anuais de produção de energia
def yearly_energy_simulation(month):
    return sum([monthly_energy_simulation(i) for i in range(1, 32)])


# Simulação de produção de energia anual por mês
yearly_energy = [yearly_energy_simulation(i) for i in range(1, 13)]

# Exibir os valores de produção de energia diária, mensal e anual
current_date = datetime.datetime.now()
day = current_date.day
month = current_date.month
year = current_date.year

# Obtém a informação do monitor
monitors = get_monitors()

caminho_csv_cidades_escolhidas = r"app/files/ids_das_cidades.csv"
# Itera sobre os monitores (em caso de vários monitores)

cidades = pd.read_sql('SELECT * FROM cidades', con=engine)

colorscale = ["#A98AA9", "#FFFFCC"]  # removi "#808080"
with open(r"app\files\geojs-35-mun.json", "r", encoding='utf-8') as e:
    geojson_file = json.load(e)

fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_file,
    locations=cidades['id'],
    z=cidades['value'],
    featureidkey="properties.id",
    colorscale=colorscale,
    showscale=False,
))

fig.update_layout(mapbox=dict(style="carto-darkmatter"), mapbox_zoom=5.5555,
                  mapbox_center={"lat": -22.5, "lon": -48}, margin=dict(l=0, r=0, t=0, b=0))

# x = ['IDGT']
# y = [100]

idgt = pd.read_sql("SELECT TOP 1 ((MGE_ENER / 1200) * (1000 / PI_ENER)) * 100 FROM PFM2022 ORDER BY E3TimeStamp DESC",
                   con=engines['UFV_Orindiuva'][0])
# Crie o gráfico de barras
fig3 = go.Figure(
    data=[go.Bar(x=['IDGT'], y=[idgt.values[0]], text=[idgt.values[0]], textposition='inside', marker_color='#cccccc')])
fig3.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                   paper_bgcolor='rgba(0, 0, 0, 0)',
                   margin=dict(l=25, r=0, t=0, b=0),
                   font=dict(color='#cccccc'),
                   yaxis_showgrid=False,
                   yaxis_showticklabels=False)

# Crie um array de valores x de 0 a 23 representando as horas do dia
# x = np.arange(24)

tempo_i_p = pd.read_sql(f"""SELECT ISI, PU, timestamp
                        FROM Central_Meteorologica
                        WHERE timestamp > "{datetime.datetime.now().strftime('%Y-%m-%d')} 00:00:00.000000"
                        AND timestamp < "{datetime.datetime.now().strftime('%Y-%m-%d')} 23:59:00.000000"
                        """, con=engine)

# Crie dois arrays de valores de "ruído" para y, um indo de 0 a 100 e o outro de 0 a 50
# y1 = np.random.normal(50, 10, 24) + np.linspace(0, 100, 24)
# y2 = np.random.normal(25, 5, 24) + np.linspace(0, 50, 24)

# Crie os gráficos Scatter
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=tempo_i_p['timestamp'].values, y=tempo_i_p['ISI'].values, mode='lines+markers',
                          name='Irradiação Solar (W/m²)', uid=1))
fig2.add_trace(go.Scatter(x=tempo_i_p['timestamp'].values, y=tempo_i_p['PU'].values, mode='lines+markers',
                          name='Potência Ativa (kW)', uid=1))

fig2.update_layout(title=None, xaxis_title='Intervalo de Tempo (Horas)',
                   yaxis_title='Irradiância',
                   legend=dict(orientation='h', y=1.175, x=0.1),
                   plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                   paper_bgcolor='rgba(0, 0, 0, 0)',
                   margin=dict(l=0, r=0, t=0, b=0),
                   font=dict(color='#cccccc')
                   )
fig2.update_xaxes(
    range=[
        f'{datetime.datetime.now().strftime("%Y-%m-%d")} 00:00:00.000000',
        f'{datetime.datetime.now().strftime("%Y-%m-%d")} 23:59:00.000000'
    ])
fig2.update_yaxes(range=[0, 3000])
inversores = [
    {"id": 1, "status": "Funcionando"},
    {"id": 2, "status": "Falha"},
    {"id": 3, "status": "Desclassificação"},
    {"id": 4, "status": "Em espera"},
    # Adicione mais inversores conforme necessário
]

num_inversores_por_aba = 2  # Número de inversores por aba
num_abas = -(-len(inversores) // num_inversores_por_aba)  # Calcula o número de abas necessárias

abas_tabela = dbc.Tabs(id='inversores', active_tab='grupo-1', children=[])

for i in range(num_abas):
    start_index = i * num_inversores_por_aba
    end_index = min((i + 1) * num_inversores_por_aba, len(inversores))
    inversores_grupo = inversores[start_index:end_index]

    table_rows = [
        html.Tr([
            html.Td(f"Inversor {inversores_grupo[i]['id']}"),
            html.Td(inversores_grupo[i]['status'])
        ]) for i in range(len(inversores_grupo))
    ]

    table = dbc.Table(
        children=[
            html.Thead(html.Tr([html.Th("Inversor"), html.Th("Status")])),
            html.Tbody(table_rows),
        ],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        # id='tabela'
    )

    aba = dbc.Tab(label=f'Grupo {i + 1}', tab_id=f'grupo-{i + 1}', children=[table])
    abas_tabela.children.append(aba)

interface = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname="/overview/")
interface.layout = dbc.Container(
    [
        # Navbar
        dbc.Row([
            navbar,
            dcc.Location(id='url', refresh=False),
        ]),
        # Conteúdo da página
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardHeader('Cidades'),
                        dcc.Graph(figure=fig, className='map', id='mapa',
                                  style={"height": f"{([m.height for m in get_monitors()][0] * 0.50)}px"})
                    ], color='dark')
                ]),
                dbc.Row([
                    dbc.Card([
                        dbc.CardHeader('Estado dos Inversores'),
                        dbc.CardBody([
                            abas_tabela
                        ], id='card-tabela'),
                    ], color='dark')
                ])
            ], sm=6),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.Row([
                            html.Fieldset([
                                dbc.CardHeader('PRODUÇÃO DA USINA'),
                                dbc.Row([
                                    dbc.CardGroup([
                                        dbc.Card([
                                            dbc.CardBody([
                                                dbc.Row([
                                                    html.Label("DIÁRIA"),
                                                ]),
                                                dbc.Row([
                                                    html.Span(id='producao-diaria')
                                                ])
                                            ])
                                        ], color='dark'),
                                        dbc.Card([
                                            dbc.CardBody([
                                                dbc.Row([
                                                    html.Label("MENSAL"),
                                                ]),
                                                dbc.Row([
                                                    html.Span(id='producao-mensal')
                                                ])
                                            ])
                                        ], color='dark'),
                                        dbc.Card([
                                            dbc.CardBody([
                                                dbc.Row([
                                                    html.Label("ANUAL"),
                                                ]),
                                                dbc.Row([
                                                    html.Span(id='producao-anual')
                                                ])
                                            ])
                                        ], color='dark')
                                    ])
                                ])
                            ]),
                        ])

                    ], color='dark', className='crd'),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader('Irradiação Diária'),
                            dbc.Row([
                                dcc.Graph(figure=fig2, className='graph', id='graphic',
                                          style={"height": f"{([m.height for m in get_monitors()][0] * 0.43)}px"}
                                          )
                            ]),
                        ], color='dark', className='crd-g'),
                    ], sm=10),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader('I.D.G.T.'),
                            dcc.Graph(figure=fig3, className='idgt',
                                      # style={"height": "100%"}
                                      )
                        ], color='dark', class_name='crd-i'),
                    ], sm=2)
                ]),
                dbc.Row([
                    dbc.Card([
                        dbc.Tabs(id='tabs', active_tab='cm', children=[
                            dbc.Tab(tab_id='cm', label='Central Meteorológica', children=[
                                dbc.CardGroup([
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('irradiação solar horizontal.png'),
                                                    top=True, className='cm-img'),
                                        dbc.CardFooter('1000.100', class_name='cm-val', id='ish')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('irradiação solar inclinada.png'),
                                                    top=True, className='cm-img'),
                                        dbc.CardFooter('1000.100', class_name='cm-val', id='isi')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('temperatura ambiente.png'), top=True,
                                                    className='cm-img'),
                                        dbc.CardFooter('99.99', class_name='cm-val', id='ta')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('temperatura das placas.png'), top=True,
                                                    className='cm-img'),
                                        dbc.CardFooter('99.99', class_name='cm-val', id='tp')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('frequência.png'), top=True,
                                                    className='cm-img'),
                                        dbc.CardFooter('60', class_name='cm-val', id='freq')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('umidade relativa do ar.png'), top=True,
                                                    className='cm-img'),
                                        dbc.CardFooter('100.99', class_name='cm-val', id='ura')
                                    ], color='dark'),
                                ])
                            ]),
                            dbc.Tab(tab_id='qgbt', label='QGBT', children=[
                                dbc.CardGroup([
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('tensão fase a-b.png'), top=True,
                                                    className='qg-img'),
                                        dbc.CardFooter('1000.100 kV', class_name='cm-val', id='a-b')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('tensão fase b-c.png'), top=True,
                                                    className='qg-img'),
                                        dbc.CardFooter('1000.100 kV', class_name='cm-val', id='b-c')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('tensão fase c-a.png'), top=True,
                                                    className='qg-img'),
                                        dbc.CardFooter('1000.100 kV', class_name='cm-val', id='c-a')
                                    ], color='dark'),
                                ])
                            ])
                        ]),
                    ], color='dark')
                ]),
            ], sm=6)
        ], className="mt-4"),
        dcc.Interval(id='intervalo', interval=6666, n_intervals=0)
    ],
    fluid=True,
)


@interface.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    # print(path)
    return path


@interface.callback(
    Output('graphic', 'figure'),
    Input('mapa', 'clickData')
)
def gera_novos_graficos_de_linha(click):
    # print(click['points'][0]['location'])
    cidades = pd.read_sql('SELECT * FROM cidades', con=engine)
    id_da_cidade_selecionada = click['points'][0]['location']
    filtro_id_selecionado_com_csv = cidades.query(f'id == {id_da_cidade_selecionada}')
    nome_usina = filtro_id_selecionado_com_csv['name'].values[0]
    if nome_usina == 'Orindiúva':
        con = orindiuva
        i_p = pd.read_sql(f"""SELECT ISI, PU, timestamp
                                FROM Central_Meteorologica
                                WHERE timestamp > "{datetime.datetime.now().strftime('%Y-%m-%d')} 00:00:00.000000"
                                AND timestamp < "{datetime.datetime.now().strftime('%Y-%m-%d')} 23:59:00.000000"
                                """, con=con)

        figura = go.Figure()
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['ISI'].values, mode='lines+markers',
                                    name='Irradiação Solar (W/m²)', uid=1))
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['PU'].values, mode='lines+markers',
                                    name='Potência Ativa (kW)', uid=1))
        figura.update_layout(title=None, xaxis_title='Intervalo de Tempo (Horas)',
                             yaxis_title='Irradiâncias',
                             legend=dict(orientation='h', y=1.175, x=0.1),
                             plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                             paper_bgcolor='rgba(0, 0, 0, 0)',
                             margin=dict(l=0, r=0, t=0, b=0),
                             font=dict(color='#cccccc')
                             )
        figura.update_xaxes(
            range=[
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 00:00:00.000000',
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 23:59:00.000000'
            ])
        figura.update_yaxes(range=[0, 3000])
        return figura
    if nome_usina == 'Elias Fausto':
        con = elias
        i_p = pd.read_sql(f"""SELECT ISI, PU, timestamp
                                FROM Central_Meteorologica
                                WHERE timestamp > "{datetime.datetime.now().strftime('%Y-%m-%d')} 00:00:00.000000"
                                AND timestamp < "{datetime.datetime.now().strftime('%Y-%m-%d')} 23:59:00.000000"
                                """, con=con)

        figura = go.Figure()
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['ISI'].values, mode='lines+markers',
                                    name='Irradiação Solar (W/m²)', uid=1))
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['PU'].values, mode='lines+markers',
                                    name='Potência Ativa (kW)', uid=1))
        figura.update_layout(title=None, xaxis_title='Intervalo de Tempo (Horas)',
                             yaxis_title='Irradiâncias',
                             legend=dict(orientation='h', y=1.175, x=0.1),
                             plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                             paper_bgcolor='rgba(0, 0, 0, 0)',
                             margin=dict(l=0, r=0, t=0, b=0),
                             font=dict(color='#cccccc')
                             )
        figura.update_xaxes(
            range=[
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 00:00:00.000000',
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 23:59:00.000000'
            ])
        figura.update_yaxes(range=[0, 3000])
        return figura
    if nome_usina == 'Monte Alto':
        con = monte
        i_p = pd.read_sql(f"""SELECT ISI, PU, timestamp
                                FROM Central_Meteorologica
                                WHERE timestamp > "{datetime.datetime.now().strftime('%Y-%m-%d')} 00:00:00.000000"
                                AND timestamp < "{datetime.datetime.now().strftime('%Y-%m-%d')} 23:59:00.000000"
                                """, con=con)

        figura = go.Figure()
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['ISI'].values, mode='lines+markers',
                                    name='Irradiação Solar (W/m²)', uid=1))
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['PU'].values, mode='lines+markers',
                                    name='Potência Ativa (kW)', uid=1))
        figura.update_layout(title=None, xaxis_title='Intervalo de Tempo (Horas)',
                             yaxis_title='Irradiâncias',
                             legend=dict(orientation='h', y=1.175, x=0.1),
                             plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                             paper_bgcolor='rgba(0, 0, 0, 0)',
                             margin=dict(l=0, r=0, t=0, b=0),
                             font=dict(color='#cccccc')
                             )
        figura.update_xaxes(
            range=[
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 00:00:00.000000',
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 23:59:00.000000'
            ])
        figura.update_yaxes(range=[0, 3000])
        return figura
    if nome_usina == 'Paraguaçu Paulista':
        con = paraguacu
        i_p = pd.read_sql(f"""SELECT ISI, PU, timestamp
                                FROM Central_Meteorologica
                                WHERE timestamp > "{datetime.datetime.now().strftime('%Y-%m-%d')} 00:00:00.000000"
                                AND timestamp < "{datetime.datetime.now().strftime('%Y-%m-%d')} 23:59:00.000000"
                                """, con=con)

        figura = go.Figure()
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['ISI'].values, mode='lines+markers',
                                    name='Irradiação Solar (W/m²)', uid=1))
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['PU'].values, mode='lines+markers',
                                    name='Potência Ativa (kW)', uid=1))
        figura.update_layout(title=None, xaxis_title='Intervalo de Tempo (Horas)',
                             yaxis_title='Irradiâncias',
                             legend=dict(orientation='h', y=1.175, x=0.1),
                             plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                             paper_bgcolor='rgba(0, 0, 0, 0)',
                             margin=dict(l=0, r=0, t=0, b=0),
                             font=dict(color='#cccccc')
                             )
        figura.update_xaxes(
            range=[
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 00:00:00.000000',
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 23:59:00.000000'
            ])
        figura.update_yaxes(range=[0, 3000])
        return figura
    if nome_usina == 'Suzano':
        con = suzano
        i_p = pd.read_sql(f"""SELECT ISI, PU, timestamp
                                FROM Central_Meteorologica
                                WHERE timestamp > "{datetime.datetime.now().strftime('%Y-%m-%d')} 00:00:00.000000"
                                AND timestamp < "{datetime.datetime.now().strftime('%Y-%m-%d')} 23:59:00.000000"
                                """, con=con)

        figura = go.Figure()
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['ISI'].values, mode='lines+markers',
                                    name='Irradiação Solar (W/m²)', uid=1))
        figura.add_trace(go.Scatter(x=i_p['timestamp'].values, y=i_p['PU'].values, mode='lines+markers',
                                    name='Potência Ativa (kW)', uid=1))
        figura.update_layout(title=None, xaxis_title='Intervalo de Tempo (Horas)',
                             yaxis_title='Irradiâncias',
                             legend=dict(orientation='h', y=1.175, x=0.1),
                             plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                             paper_bgcolor='rgba(0, 0, 0, 0)',
                             margin=dict(l=0, r=0, t=0, b=0),
                             font=dict(color='#cccccc')
                             )
        figura.update_xaxes(
            range=[
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 00:00:00.000000',
                f'{datetime.datetime.now().strftime("%Y-%m-%d")} 23:59:00.000000'
            ])
        figura.update_yaxes(range=[0, 3000])
        return figura
        # df = pd.read_sql('SELECT * FROM obra_cm_invs')


# Função para salvar os dados no MySQL

@interface.callback(
    Output('logo-usina', 'brand'),
    Input('mapa', 'clickData')
)
def troca_nome_de_usina(cidade_selecionada):
    cidades = pd.read_sql('SELECT * FROM cidades', con=create_engine('sqlite:///./database/database.db'))
    return cidades.query(f'id == {cidade_selecionada["points"][0]["location"]}')['name'].values[0]


@interface.callback(
    Output('producao-diaria', 'children'),
    Output('producao-mensal', 'children'),
    Output('producao-anual', 'children'),
    Input('mapa', 'clickData')
)
def mostra_producoes_de_energia(cidade_selecionada):
    def retorna_unidade(valor):
        return f'{round(round(valor, 1), 1)} kW'

    cidades = pd.read_sql('SELECT * FROM cidades', con=engine)

    id_cidade_selecionada = cidade_selecionada['points'][0]['location']
    id_cidade_csv = cidades.query(f"id == {id_cidade_selecionada}")
    if id_cidade_csv['name'].values[0] in ['Orindiuva', 'Elias Fausto', 'Monte Alto', 'Paraguaçu Paulista', 'Suzano']:
        data_atual = datetime.datetime.now()
        hora_atual = data_atual.hour
        dia_atual = data_atual.day
        mes_atual = data_atual.month
        ano_atual = data_atual.year

        return "-", "-", "-"


cliente_modbus_de_paragucu = ModbusTcpClient('191.242.49.24', port=1002)
cliente_modbus_de_suzano = ModbusTcpClient('45.182.195.252', port=1002)
cliente_modbus_de_monte = ModbusTcpClient('45.170.209.104', port=1002)
cliente_modbus_de_elias = ModbusTcpClient('177.101.74.222', port=1002)
cliente_modbus_de_orindiuva = ModbusTcpClient('45.176.175.27', port=1002)
cliente_modbus_de_elias2 = ModbusTcpClient('177.101.74.222', port=502)
cliente_modbus_de_orindiuva2 = ModbusTcpClient('45.176.175.27', port=502)

lista_modbus = [cliente_modbus_de_suzano, cliente_modbus_de_monte, cliente_modbus_de_paragucu]


def ler_dados_da_cm(registro, cliente):
    try:
        val = cliente.read_holding_registers(registro, 2, slave=1 if cliente in lista_modbus else 10)
        dec = BinaryPayloadDecoder.fromRegisters(val.registers,
                                                 byteorder=Endian.LITTLE if cliente in lista_modbus else Endian.BIG,
                                                 wordorder=Endian.BIG if cliente in lista_modbus else Endian.LITTLE)
        final = dec.decode_32bit_float()
        return final
    except Exception as e:
        return 0


@interface.callback(
    Output('ish', 'children'),
    Output('isi', 'children'),
    Output('ta', 'children'),
    Output('tp', 'children'),
    Output('ura', 'children'),
    Output('freq', 'children'),
    Output('a-b', 'children'),
    Output('b-c', 'children'),
    Output('c-a', 'children'),
    Input('tabs', 'active_tab'),
    Input('intervalo', 'n_intervals'),
    Input('mapa', 'clickData'),
)
def mostrar_valores_da_centrak_meteorologica(aba, itvl, clickData):
    if aba in ['cm', 'qgbt']:
        id_usina = clickData['points'][0]['location']
        nome_usina = cidades.query(f"id == {id_usina}")['name'].values[0]
        if nome_usina == 'Orindiúva':
            client = cliente_modbus_de_orindiuva
            lista = [237, 223, 225, 233, 227]
            return round(ler_dados_da_cm(lista[0], client)), \
                round(ler_dados_da_cm(lista[1], client)), \
                round(ler_dados_da_cm(lista[2], client)), \
                round(ler_dados_da_cm(lista[3], client)), \
                round(ler_dados_da_cm(lista[4], client)), \
                "-", "-", "-", "-"
        if nome_usina == 'Elias Fausto':
            lista = [223, 225, 227, 235, 229]
            client = cliente_modbus_de_elias
            return round(ler_dados_da_cm(lista[0], client)), \
                round(ler_dados_da_cm(lista[1], client)), \
                round(ler_dados_da_cm(lista[2], client)), \
                round(ler_dados_da_cm(lista[3], client)), \
                round(ler_dados_da_cm(lista[4], client)), \
                "-", "-", "-", "-"
        if nome_usina == 'Monte Alto':
            lista = [1, 3, 5, 9]
            client = cliente_modbus_de_monte
            return round(ler_dados_da_cm(lista[0], client)), \
                round(ler_dados_da_cm(lista[1], client)), \
                round(ler_dados_da_cm(lista[2], client)), \
                round(ler_dados_da_cm(lista[3], client)), \
                "-", "-", "-", "-", '-'
            # round(ler_dados_da_cm(lista[4], client)), \
        if nome_usina == 'Paraguaçu Paulista':
            lista = [1, 3, 5, 9, None]
            client = cliente_modbus_de_paragucu
            return round(ler_dados_da_cm(lista[0], client)), \
                round(ler_dados_da_cm(lista[1], client)), \
                round(ler_dados_da_cm(lista[2], client)), \
                round(ler_dados_da_cm(lista[3], client)), \
                "-", "-", "-", "-", '-'
            # round(ler_dados_da_cm(lista[4], client)), \
        if nome_usina == 'Suzano':
            lista = [1, 3, 5, 9, None]
            client = cliente_modbus_de_suzano
            return round(ler_dados_da_cm(lista[0], client)), \
                round(ler_dados_da_cm(lista[1], client)), \
                round(ler_dados_da_cm(lista[2], client)), \
                round(ler_dados_da_cm(lista[3], client)), \
                "-", "-", "-", "-", '-'
            # round(ler_dados_da_cm(lista[4], client)), \
    raise PreventUpdate


def ler_os_estados_dos_inversores(registro, cliente_modbus):
    try:
        if cliente_modbus in lista_modbus:
            leitura = cliente_modbus.read_holding_registers(registro, 2, slave=1)
            decodificacao = BinaryPayloadDecoder.fromRegisters(leitura.registers, byteorder=Endian.BIG,
                                                               wordorder=Endian.LITTLE)
            conversao = decodificacao.decode_16bit_int()
            print(f"pp/su/ma:{conversao}")

            if conversao == 0:
                return 'Em espera'
            if conversao == 1:
                return 'Gerando'
            if conversao == 2:
                return 'Falha'
            if conversao == 3:
                return 'Falha permanente'
            if conversao == 6 or conversao == 4:
                return 'Não encontrado'
        else:
            val = cliente_modbus.read_input_registers(5037, 2, slave=registro)
            dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
            final = dec.decode_32bit_uint()
            if final == 0:
                return "Funcionando"

            elif final == 4864:
                return "Chave de parada"

            elif final == 5376:
                return "Parada de emergência"

            elif final == 4608:
                return "Iniciando espera"

            elif final == 5120 or final == 5210:
                return "Em espera"

            elif final == 5632:
                return "Partindo"

            elif final == 9472:
                return "Falha de comunicação"

            elif final == 21760:
                return "Falha"

            elif final == 32768:
                return "Parado"

            elif final == 33024:
                return "Desclassificação"

            elif final == 33280:
                return "Expedição"

            elif final == 37120:
                return "Alarme ativo"

    except Exception as e:
        print(e)
        return "Erro"


@interface.callback(
    Output('card-tabela', 'children'),
    Input('intervalo', 'n_intervals'),
    Input('mapa', 'clickData'),
)
def mostrar_inversores(n, clique):
    id_usina = clique['points'][0]['location']
    nome_usina = cidades.query(f"id == {id_usina}")['name'].values[0]
    if nome_usina == 'Orindiúva':
        inv1 = ler_os_estados_dos_inversores(4, cliente_modbus_de_orindiuva2)
        inv2 = ler_os_estados_dos_inversores(1, cliente_modbus_de_orindiuva2)
        inv3 = ler_os_estados_dos_inversores(3, cliente_modbus_de_orindiuva2)
        inv4 = ler_os_estados_dos_inversores(2, cliente_modbus_de_orindiuva2)
        invs = [
            {"id": 1, "status": inv1},
            {"id": 2, "status": inv2},
            {"id": 3, "status": inv3},
            {"id": 4, "status": inv4},
            # Adicione mais inversores conforme necessário
        ]
        inversores_por_aba = 2  # Número de inversores por aba
        abas = -(-len(invs) // inversores_por_aba)  # Calcula o número de abas necessárias

        tabela = dbc.Tabs(id='inversores', active_tab='grupo-1', children=[])

        for i in range(abas):
            start = i * inversores_por_aba
            end = min((i + 1) * inversores_por_aba, len(invs))
            grupo = invs[start:end]

            rows = [
                html.Tr([
                    html.Td(f"Inversor {grupo[i]['id']}"),
                    html.Td(grupo[i]['status'])
                ]) for i in range(len(grupo))
            ]

            tbl = dbc.Table(
                children=[
                    html.Thead(html.Tr([html.Th("Inversor"), html.Th("Status")])),
                    html.Tbody(rows),
                ],
                bordered=True,
                hover=True,
                responsive=True,
                striped=True,
                # id='tabela'
            )

            aba = dbc.Tab(label=f'Grupo {i + 1}', tab_id=f'grupo-{i + 1}', children=[tbl])
            tabela.children.append(aba)

        return tabela
    if nome_usina == 'Elias Fausto':
        inv1 = ler_os_estados_dos_inversores(1, cliente_modbus_de_elias2)
        inv2 = ler_os_estados_dos_inversores(2, cliente_modbus_de_elias2)
        inv3 = ler_os_estados_dos_inversores(3, cliente_modbus_de_elias2)
        inv4 = ler_os_estados_dos_inversores(4, cliente_modbus_de_elias2)
        invs = [
            {"id": 1, "status": inv1},
            {"id": 2, "status": inv2},
            {"id": 3, "status": inv3},
            {"id": 4, "status": inv4},
            # Adicione mais inversores conforme necessário
        ]
        inversores_por_aba = 2  # Número de inversores por aba
        abas = -(-len(invs) // inversores_por_aba)  # Calcula o número de abas necessárias

        tabela = dbc.Tabs(id='inversores', active_tab='grupo-1', children=[])

        for i in range(abas):
            start = i * inversores_por_aba
            end = min((i + 1) * inversores_por_aba, len(invs))
            grupo = invs[start:end]

            rows = [
                html.Tr([
                    html.Td(f"Inversor {grupo[i]['id']}"),
                    html.Td(grupo[i]['status'])
                ]) for i in range(len(grupo))
            ]

            tbl = dbc.Table(
                children=[
                    html.Thead(html.Tr([html.Th("Inversor"), html.Th("Status")])),
                    html.Tbody(rows),
                ],
                bordered=True,
                hover=True,
                responsive=True,
                striped=True,
                # id='tabela'
            )

            aba = dbc.Tab(label=f'Grupo {i + 1}', tab_id=f'grupo-{i + 1}', children=[tbl])
            tabela.children.append(aba)

        return tabela

    if nome_usina == 'Monte Alto':
        inv1 = ler_os_estados_dos_inversores(157, cliente_modbus_de_monte)
        inv2 = ler_os_estados_dos_inversores(257, cliente_modbus_de_monte)
        inv3 = ler_os_estados_dos_inversores(357, cliente_modbus_de_monte)
        inv4 = ler_os_estados_dos_inversores(457, cliente_modbus_de_monte)
        invs = [
            {"id": 1, "status": inv1},
            {"id": 2, "status": inv2},
            {"id": 3, "status": inv3},
            {"id": 4, "status": inv4},
            # Adicione mais inversores conforme necessário
        ]
        inversores_por_aba = 2  # Número de inversores por aba
        abas = -(-len(invs) // inversores_por_aba)  # Calcula o número de abas necessárias

        tabela = dbc.Tabs(id='inversores', active_tab='grupo-1', children=[])

        for i in range(abas):
            start = i * inversores_por_aba
            end = min((i + 1) * inversores_por_aba, len(invs))
            grupo = invs[start:end]

            rows = [
                html.Tr([
                    html.Td(f"Inversor {grupo[i]['id']}"),
                    html.Td(grupo[i]['status'])
                ]) for i in range(len(grupo))
            ]

            tbl = dbc.Table(
                children=[
                    html.Thead(html.Tr([html.Th("Inversor"), html.Th("Status")])),
                    html.Tbody(rows),
                ],
                bordered=True,
                hover=True,
                responsive=True,
                striped=True,
                # id='tabela'
            )

            aba = dbc.Tab(label=f'Grupo {i + 1}', tab_id=f'grupo-{i + 1}', children=[tbl])
            tabela.children.append(aba)

        return tabela

    if nome_usina == 'Paraguaçu Paulista':
        inv1 = ler_os_estados_dos_inversores(157, cliente_modbus_de_paragucu)
        inv2 = ler_os_estados_dos_inversores(257, cliente_modbus_de_paragucu)
        inv3 = ler_os_estados_dos_inversores(357, cliente_modbus_de_paragucu)
        inv4 = ler_os_estados_dos_inversores(457, cliente_modbus_de_paragucu)
        inv5 = ler_os_estados_dos_inversores(557, cliente_modbus_de_paragucu)
        inv6 = ler_os_estados_dos_inversores(657, cliente_modbus_de_paragucu)
        inv7 = ler_os_estados_dos_inversores(757, cliente_modbus_de_paragucu)
        inv8 = ler_os_estados_dos_inversores(857, cliente_modbus_de_paragucu)
        invs = [
            {"id": 1, "status": inv1},
            {"id": 2, "status": inv2},
            {"id": 3, "status": inv3},
            {"id": 4, "status": inv4},
            {"id": 5, "status": inv5},
            {"id": 6, "status": inv6},
            {"id": 7, "status": inv7},
            {"id": 8, "status": inv8},
            # Adicione mais inversores conforme necessário
        ]
        inversores_por_aba = 2  # Número de inversores por aba
        abas = -(-len(invs) // inversores_por_aba)  # Calcula o número de abas necessárias

        tabela = dbc.Tabs(id='inversores', active_tab='grupo-1', children=[])

        for i in range(abas):
            start = i * inversores_por_aba
            end = min((i + 1) * inversores_por_aba, len(invs))
            grupo = invs[start:end]

            rows = [
                html.Tr([
                    html.Td(f"Inversor {grupo[i]['id']}"),
                    html.Td(grupo[i]['status'])
                ]) for i in range(len(grupo))
            ]

            tbl = dbc.Table(
                children=[
                    html.Thead(html.Tr([html.Th("Inversor"), html.Th("Status")])),
                    html.Tbody(rows),
                ],
                bordered=True,
                hover=True,
                responsive=True,
                striped=True,
                # id='tabela'
            )

            aba = dbc.Tab(label=f'Grupo {i + 1}', tab_id=f'grupo-{i + 1}', children=[tbl])
            tabela.children.append(aba)

        return tabela

    if nome_usina == 'Suzano':
        inv1 = ler_os_estados_dos_inversores(157, cliente_modbus_de_suzano)
        inv2 = ler_os_estados_dos_inversores(257, cliente_modbus_de_suzano)
        inv3 = ler_os_estados_dos_inversores(357, cliente_modbus_de_suzano)
        inv4 = ler_os_estados_dos_inversores(457, cliente_modbus_de_suzano)
        inv5 = ler_os_estados_dos_inversores(557, cliente_modbus_de_suzano)
        inv6 = ler_os_estados_dos_inversores(657, cliente_modbus_de_suzano)
        inv7 = ler_os_estados_dos_inversores(757, cliente_modbus_de_suzano)
        inv8 = ler_os_estados_dos_inversores(857, cliente_modbus_de_suzano)
        invs = [
            {"id": 1, "status": inv1},
            {"id": 2, "status": inv2},
            {"id": 3, "status": inv3},
            {"id": 4, "status": inv4},
            {"id": 5, "status": inv5},
            {"id": 6, "status": inv6},
            {"id": 7, "status": inv7},
            {"id": 8, "status": inv8},
            # Adicione mais inversores conforme necessário
        ]
        inversores_por_aba = 2  # Número de inversores por aba
        abas = -(-len(invs) // inversores_por_aba)  # Calcula o número de abas necessárias

        tabela = dbc.Tabs(id='inversores', active_tab='grupo-1', children=[])

        for i in range(abas):
            start = i * inversores_por_aba
            end = min((i + 1) * inversores_por_aba, len(invs))
            grupo = invs[start:end]

            rows = [
                html.Tr([
                    html.Td(f"Inversor {grupo[i]['id']}"),
                    html.Td(grupo[i]['status'])
                ]) for i in range(len(grupo))
            ]

            tbl = dbc.Table(
                children=[
                    html.Thead(html.Tr([html.Th("Inversor"), html.Th("Status")])),
                    html.Tbody(rows),
                ],
                bordered=True,
                hover=True,
                responsive=True,
                striped=True,
                # id='tabela'
            )

            aba = dbc.Tab(label=f'Grupo {i + 1}', tab_id=f'grupo-{i + 1}', children=[tbl])
            tabela.children.append(aba)

        return tabela
    raise PreventUpdate
