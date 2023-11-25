import json
from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from app.templates.partials.index import sidebar, navbar, autenticacao
from screeninfo import get_monitors
from sqlalchemy import create_engine

import numpy as np
import datetime


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

# print(f"Produção de energia diária atual: {daily_energy[datetime.datetime.now().hour]:.2f} kWs")
# print(f"Produção de energia mensal atual: {monthly_energy[day - 1]:.2f} kWs")
# print(f"Produção de energia anual atual: {yearly_energy[month - 1]:.2f} kWs")

# Obtém a informação do monitor
monitors = get_monitors()

caminho_csv_cidades_escolhidas = r"app/files/ids_das_cidades.csv"
# Itera sobre os monitores (em caso de vários monitores)
# for m in monitors:
#     print("Largura:", m.width, "Altura:", m.height)

df = pd.read_csv(r"app\files\saida_atualizado.csv")

colorscale = ["#A98AA9", "#FFFFCC"]  # removi "#808080"
with open(r"app\files\geojs-35-mun.json", "r", encoding='utf-8') as e:
    geojson_file = json.load(e)

fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_file,
    locations=df['id'],
    z=df['value'],
    featureidkey="properties.id",
    colorscale=colorscale,
    showscale=False,
))

fig.update_layout(mapbox=dict(style="carto-darkmatter"), mapbox_zoom=6.66666,
                  mapbox_center={"lat": -23.3055, "lon": -45.967}, margin=dict(l=0, r=0, t=0, b=0))

x = ['IDGT']
y = [100]

# Crie o gráfico de barras
fig3 = go.Figure(data=[go.Bar(x=x, y=y, text=y, textposition='inside', marker_color='#cccccc')])
fig3.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                   paper_bgcolor='rgba(0, 0, 0, 0)',
                   margin=dict(l=25, r=0, t=0, b=0),
                   font=dict(color='#cccccc'),
                   yaxis_showgrid=False,
                   yaxis_showticklabels=False)

# Crie um array de valores x de 0 a 23 representando as horas do dia
x = np.arange(24)

# Crie dois arrays de valores de "ruído" para y, um indo de 0 a 100 e o outro de 0 a 50
y1 = np.random.normal(50, 10, 24) + np.linspace(0, 100, 24)
y2 = np.random.normal(25, 5, 24) + np.linspace(0, 50, 24)

# Crie os gráficos Scatter
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers', name='Irradiação Solar (Local 1)', uid=1))
fig2.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers', name='Irradiação Solar (Local 2)', uid=2))

fig2.update_layout(title=None, xaxis_title='Intervalo de Tempo (Horas)',
                   yaxis_title='Irradiâncias',
                   legend=dict(orientation='h', y=1.175, x=0.1),
                   plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                   paper_bgcolor='rgba(0, 0, 0, 0)',
                   margin=dict(l=0, r=0, t=0, b=0),
                   font=dict(color='#cccccc')
                   )
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
            html.Td(f"Inversor {inversor['id']}"),
            html.Td(inversor['status'])
        ]) for inversor in inversores_grupo
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
    )

    aba = dbc.Tab(label=f'Grupo {i + 1}', tab_id=f'grupo-{i + 1}', children=[table])
    abas_tabela.children.append(aba)

interface = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname="/interface/")
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
                        abas_tabela
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
                        dbc.Tabs(active_tab='cm', children=[
                            dbc.Tab(tab_id='cm', label='Central Meteorológica', children=[
                                dbc.CardGroup([
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('irradiação solar horizontal.png'),
                                                    top=True, className='cm-img'),
                                        dbc.CardFooter('1000.100', class_name='cm-val')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('irradiação solar inclinada.png'),
                                                    top=True, className='cm-img'),
                                        dbc.CardFooter('1000.100', class_name='cm-val')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('temperatura ambiente.png'), top=True,
                                                    className='cm-img'),
                                        dbc.CardFooter('99.99', class_name='cm-val')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('temperatura das placas.png'), top=True,
                                                    className='cm-img'),
                                        dbc.CardFooter('99.99', class_name='cm-val')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('frequência.png'), top=True,
                                                    className='cm-img'),
                                        dbc.CardFooter('60', class_name='cm-val')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('umidade relativa do ar.png'), top=True,
                                                    className='cm-img'),
                                        dbc.CardFooter('100.99', class_name='cm-val')
                                    ], color='dark'),
                                ])
                            ]),
                            dbc.Tab(tab_id='qgbt', label='QGBT', children=[
                                dbc.CardGroup([
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('tensão fase a-b.png'), top=True,
                                                    className='qg-img'),
                                        dbc.CardFooter('1000.100 kV', class_name='cm-val')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('tensão fase b-c.png'), top=True,
                                                    className='qg-img'),
                                        dbc.CardFooter('1000.100 kV', class_name='cm-val')
                                    ], color='dark'),
                                    dbc.Card([
                                        dbc.CardImg(src=interface.get_asset_url('tensão fase c-a.png'), top=True,
                                                    className='qg-img'),
                                        dbc.CardFooter('1000.100 kV', class_name='cm-val')
                                    ], color='dark'),
                                ])
                            ])
                        ]),
                    ], color='dark')
                ]),
            ], sm=6)
        ], className="mt-4"),
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
    id_da_cidade_selecionada = click['points'][0]['location']
    filtro_id_selecionado_com_csv = df.query(f'id == {id_da_cidade_selecionada}')
    nome_usina = filtro_id_selecionado_com_csv['name'].values[0]
    if nome_usina == 'Jacareí':
        x_novo = np.arange(24)

        y1_novo = np.random.normal(50, 10, 24) + np.linspace(0, 100, 24)
        y2_novo = np.random.normal(25, 5, 24) + np.linspace(0, 50, 24)

        grafico_irradiancia_potencia_atualizado = go.Figure()
        grafico_irradiancia_potencia_atualizado.add_trace(
            go.Scatter(
                x=x_novo,
                y=y1_novo,
                mode='lines+markers',
                name='Irradiância'
            ))
        grafico_irradiancia_potencia_atualizado.add_trace(
            go.Scatter(
                x=x_novo,
                y=y2_novo,
                mode='lines+markers',
                name='Potência'
            ))
        grafico_irradiancia_potencia_atualizado.update_layout(title=None, xaxis_title='Intervalo de Tempo (Horas)',
                                                              yaxis_title='Irradiâncias',
                                                              legend=dict(orientation='h', y=1.175, x=0.1),
                                                              plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                                                              paper_bgcolor='rgba(0, 0, 0, 0)',
                                                              margin=dict(l=0, r=0, t=0, b=0),
                                                              font=dict(color='#cccccc')
                                                              )
        return grafico_irradiancia_potencia_atualizado

# Função para salvar os dados no MySQL

@interface.callback(
    Output('logo-usina', 'brand'),
    Input('mapa', 'clickData')
)
def troca_nome_de_usina(cidade_selecionada):
    return df.query(f'id == {cidade_selecionada["points"][0]["location"]}')['name'].values[0]


@interface.callback(
    Output('producao-diaria', 'children'),
    Output('producao-mensal', 'children'),
    Output('producao-anual', 'children'),
    Input('mapa', 'clickData')
)
def mostra_producoes_de_energia(cidade_selecionada):
    def retorna_unidade(valor):
        return f'{round(round(valor, 1), 1)} kW'

    id_cidade_selecionada = cidade_selecionada['points'][0]['location']
    id_cidade_csv = df.query(f"id == {id_cidade_selecionada}")
    if id_cidade_csv['name'].values[0] == 'Jacareí':
        data_atual = datetime.datetime.now()
        hora_atual = data_atual.hour
        dia_atual = data_atual.day
        mes_atual = data_atual.month
        ano_atual = data_atual.year

        return retorna_unidade(daily_energy_simulation(hora_atual)), \
            retorna_unidade(monthly_energy_simulation(None)), \
            retorna_unidade(yearly_energy_simulation(None))


# autenticacao(interface)
