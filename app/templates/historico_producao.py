import datetime
import json

import dash
import pandas as pd
from screeninfo import get_monitors
from sqlalchemy import create_engine

from app import app
from app.templates.partials.index import navbar
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

engine = create_engine('sqlite:///./database/database.db')

cidades = pd.read_sql('SELECT * FROM cidades', con=engine)

colorscale = ["#A98AA9", "#FFFFCC"]  # removi "#808080"
with open(r"app\geojsons\sudeste\sp\geojs-35-mun.json", "r", encoding='utf-8') as e:
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
# Crie uma instância do aplicativo Dash
historico_producao = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR],
                          url_base_pathname='/historico_producao/')


inicio = pd.read_sql("SELECT timestamp FROM Estado_Inversores ORDER BY timestamp ASC LIMIT 1", con=create_engine("sqlite:///./database/orindiuva.db"))

# Layout do corpo da tela
historico_producao.layout = dbc.Container(
    [
        navbar,
        dcc.Location(id='url', refresh=False),
        html.H1('Histórico de Produção de Energia', className="text-center my-4"),
        dbc.Row(
            [
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Selecione as datas"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dcc.DatePickerRange(
                                        id='data-producao',
                                        min_date_allowed=datetime.date(1969, 12, 31),
                                        max_date_allowed=datetime.datetime.now().strftime("%Y-%m-%d"),
                                        initial_visible_month=inicio['timestamp'].values[0]
                                    )
                                ], sm=6),
                                dbc.Col([
                                    dbc.Button('Gerar Relatório', id='gerar', disabled=True),
                                    dcc.Download(id='download')
                                ], sm=6, style={'text-align': 'center'})
                            ]),
                            dbc.Row(id='output-grafico-historico')
                        ])
                    ])
                ], sm=6),
                dbc.Col(
                    [
                        dbc.Card([
                            dbc.CardHeader("Selecione uma cidade", id='cidade-selecionada'),
                            dbc.CardBody([
                                dcc.Graph(figure=fig, className='map', id='mapa',
                                          style={"height": f"{get_monitors()[0].height * 0.66}px"})
                            ])
                        ])
                    ],
                    sm=6,
                ),
            ],
            className="my-4",
        ),
    ],
    fluid=True,
)


# Callback para atualizar o gráfico com os dados históricos

# Callback para atualizar o gráfico com os dados históricos
# @historico_producao.callback(
#     Output('output-grafico-historico', 'children'),
#     Output('gerar', 'disabled'),
#     [
#         Input('data-producao', 'start_date'),
#         Input('data-producao', 'end_date'),
#         Input('gerar', 'n_clicks'),
#         Input('mapa', 'clickData'),
#     ]
# )
# def plota_producao(comeco, fim, gerar, mapa):
#     cities = pd.read_sql('SELECT * FROM cidades', con=engine)
#     id_ = mapa['points'][0]['location']
#     print(id)
#     print(cities)
#     filtro = cities[cities['id'] == id_]['name'].values[0]
#     print(filtro)
#     if comeco and fim:
#         if filtro == 'Orindiúva':
#             cnxn = create_engine("sqlite:///./database/orindiuva.db")
#             data = pd.read_sql(
#                 f"SELECT ISI, PU, timestamp FROM Central_Meteorologica WHERE timestamp > '{comeco} 00:00:00.000000' AND timestamp < '{fim} 23:59:00.000000'", con=cnxn)
#             print(data['ISI'])
#             print(data['PU'])
#             figura = go.Figure()
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['ISI'].values, mode='lines', name='Irradiância'))
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['PU'].values, mode='lines', name='Potência Ativa'))
#             figura.update_layout(title='Histórico de Produção de Energia',
#                                  plot_bgcolor='rgba(0, 0, 0, 0)',
#                                  paper_bgcolor='rgba(0, 0, 0, 0)',
#                                  font_color='white',
#                                  height=get_monitors()[0].height * 0.5975)
#             figura.update_xaxes(range=[
#                 f'{comeco} 00:00:00.000000',
#                 f'{comeco} 23:59:00.000000',
#             ])
#             figura.update_yaxes(range=[0, 1500])
#             return dcc.Graph(figure=figura, config={'displayModeBar': False}), False
#         if filtro == 'Elias Fausto':
#             cnxn = create_engine("sqlite:///./database/elias_fausto.db")
#             data = pd.read_sql(
#                 f"SELECT ISI, PU, timestamp FROM Central_Meteorologica WHERE timestamp > '{comeco} 00:00:00.000000' AND timestamp < '{fim} 23:59:00.000000'", con=cnxn)
#             figura = go.Figure()
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['ISI'].values, mode='lines', name='Irradiância'))
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['PU'].values, mode='lines', name='Potência Ativa'))
#             figura.update_layout(title='Histórico de Produção de Energia',
#                                  plot_bgcolor='rgba(0, 0, 0, 0)',
#                                  paper_bgcolor='rgba(0, 0, 0, 0)',
#                                  font_color='white',
#                                  height=get_monitors()[0].height * 0.5975)
#             figura.update_xaxes(range=[
#                 f'{comeco} 00:00:00.000000',
#                 f'{comeco} 23:59:00.000000',
#             ])
#             figura.update_yaxes(range=[0, 1500])
#             return dcc.Graph(figure=figura, config={'displayModeBar': False}), False
#         if filtro == 'Monte Alto':
#             cnxn = create_engine("sqlite:///./database/monte_alto.db")
#             data = pd.read_sql(
#                 f"SELECT ISI, PU, timestamp FROM Central_Meteorologica WHERE timestamp > '{comeco} 00:00:00.000000' AND timestamp < '{fim} 23:59:00.000000'", con=cnxn)
#             figura = go.Figure()
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['ISI'].values, mode='lines', name='Irradiância'))
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['PU'].values, mode='lines', name='Potência Ativa'))
#             figura.update_layout(title='Histórico de Produção de Energia',
#                                  plot_bgcolor='rgba(0, 0, 0, 0)',
#                                  paper_bgcolor='rgba(0, 0, 0, 0)',
#                                  font_color='white',
#                                  height=get_monitors()[0].height * 0.5975)
#             figura.update_xaxes(range=[
#                 f'{comeco} 00:00:00.000000',
#                 f'{comeco} 23:59:00.000000',
#             ])
#             figura.update_yaxes(range=[0, 1500])
#             return dcc.Graph(figure=figura, config={'displayModeBar': False}), False
#         if filtro == 'Suzano':
#             cnxn = create_engine("sqlite:///./database/suzano.db")
#             data = pd.read_sql(
#                 f"SELECT ISI, PU, timestamp FROM Central_Meteorologica WHERE timestamp > '{comeco} 00:00:00.000000' AND timestamp < '{fim} 23:59:00.000000'", con=cnxn)
#             figura = go.Figure()
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['ISI'].values, mode='lines', name='Irradiância'))
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['PU'].values, mode='lines', name='Potência Ativa'))
#             figura.update_layout(title='Histórico de Produção de Energia',
#                                  plot_bgcolor='rgba(0, 0, 0, 0)',
#                                  paper_bgcolor='rgba(0, 0, 0, 0)',
#                                  font_color='white',
#                                  height=get_monitors()[0].height * 0.5975)
#             figura.update_xaxes(range=[
#                 f'{comeco} 00:00:00.000000',
#                 f'{comeco} 23:59:00.000000',
#             ])
#             figura.update_yaxes(range=[0, 2250])
#             return dcc.Graph(figure=figura, config={'displayModeBar': False}), False
#         if filtro == 'Paraguaçu Paulista':
#             cnxn = create_engine("sqlite:///./database/paraguacu.db")
#             data = pd.read_sql(
#                 f"SELECT ISI, PU, timestamp FROM Central_Meteorologica WHERE timestamp > '{comeco} 00:00:00.000000' AND timestamp < '{fim} 23:59:00.000000'", con=cnxn)
#             figura = go.Figure()
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['ISI'].values, mode='lines', name='Irradiância'))
#             figura.add_trace(go.Scatter(x=data['timestamp'].values, y=data['PU'].values, mode='lines', name='Potência Ativa'))
#             figura.update_layout(title='Histórico de Produção de Energia',
#                                  plot_bgcolor='rgba(0, 0, 0, 0)',
#                                  paper_bgcolor='rgba(0, 0, 0, 0)',
#                                  font_color='white',
#                                  height=get_monitors()[0].height * 0.5975)
#             figura.update_xaxes(range=[
#                 f'{comeco} 00:00:00.000000',
#                 f'{comeco} 23:59:00.000000',
#             ])
#             figura.update_yaxes(range=[0, 2250])
#             return dcc.Graph(figure=figura, config={'displayModeBar': False}), False


@historico_producao.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path


@historico_producao.callback(
    Output('cidade-selecionada', 'children'),
    Input('mapa', 'clickData')
)
def mostra_nome_cidade(dados_cidade):
    df = pd.read_sql('SELECT * FROM cidades', con=engine)
    return f"""Cidade {df.query(f"id == {dados_cidade['points'][0]['location']}")["name"].values[0]} selecionada"""


# @historico_producao.callback(
#     Output('download', 'data'),
#     Input('gerar', 'n_clicks'),
#     Input('mapa', 'clickData'),
#     Input('data-producao', 'start_date'),
#     Input('data-producao', 'end_date'),
# )
# def baixar_planilha(btn, clique, comeco, fim):
#     selecionei = clique['points'][0]['location']
#     city = pd.read_sql('SELECT * FROM cidades', con=create_engine('sqlite:///./database/database.db'))
#     filtro = city[city['id'] == selecionei]['name'].values[0]
#     if dash.ctx.triggered_id == 'gerar':
#         if filtro == 'Elias Fausto':
#             engine = create_engine('sqlite:///./database/elias_fausto.db')
#             conteudo = pd.read_sql(f"""
#             SELECT ISI, PU, timestamp
#             FROM Central_Meteorologica
#             WHERE timestamp > '{comeco} 00:00:00.000000'
#             AND timestamp < '{fim} 23:59:00.000000'
#             """, con=engine)
#             return dcc.send_data_frame(conteudo.to_excel, f'relatório_excel_{filtro}_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.xlsx', index=False)
#         if filtro == 'Monte Alto':
#             engine = create_engine('sqlite:///./database/monte_alto.db')
#             conteudo = pd.read_sql(f"""
#                     SELECT ISI, PU, timestamp
#                     FROM Central_Meteorologica
#                     WHERE timestamp > '{comeco} 00:00:00.000000'
#                     AND timestamp < '{fim} 23:59:00.000000'
#                     """, con=engine)
#             return dcc.send_data_frame(conteudo.to_excel, f'relatório_excel_{filtro}_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.xlsx', index=False)
#
#         if filtro == 'Orindiúva':
#             engine = create_engine('sqlite:///./database/orindiuva.db')
#             conteudo = pd.read_sql(f"""
#                     SELECT ISI, PU, timestamp
#                     FROM Central_Meteorologica
#                     WHERE timestamp > '{comeco} 00:00:00.000000'
#                     AND timestamp < '{fim} 23:59:00.000000'
#                     """, con=engine)
#             return dcc.send_data_frame(conteudo.to_excel, f'relatório_excel_{filtro}_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.xlsx', index=False)
#
#         if filtro == 'Paraguaçu Paulista':
#             engine = create_engine('sqlite:///./database/paraguacu.db')
#             conteudo = pd.read_sql(f"""
#                     SELECT ISI, PU, timestamp
#                     FROM Central_Meteorologica
#                     WHERE timestamp > '{comeco} 00:00:00.000000'
#                     AND timestamp < '{fim} 23:59:00.000000'
#                     """, con=engine)
#             return dcc.send_data_frame(conteudo.to_excel, f'relatório_excel_{filtro}_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.xlsx', index=False)
#
#         if filtro == 'Suzano':
#             engine = create_engine('sqlite:///./database/suzano.db')
#             conteudo = pd.read_sql(f"""
#                     SELECT ISI, PU, timestamp
#                     FROM Central_Meteorologica
#                     WHERE timestamp > '{comeco} 00:00:00.000000'
#                     AND timestamp < '{fim} 23:59:00.000000'
#                     """, con=engine)
#             return dcc.send_data_frame(conteudo.to_excel, f'relatório_excel_{filtro}_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.xlsx', index=False)
