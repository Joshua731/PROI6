import json

import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate
from sqlalchemy import create_engine

from app import app
from dash import ctx, Dash, dcc, html, Input, Output
import plotly.graph_objects as go


def plotar_mapa_de_edicao():
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
        colorscale='algae',
        showscale=False,
    ))

    fig.update_layout(mapbox=dict(style="carto-darkmatter"), mapbox_zoom=5.5555,
                      mapbox_center={"lat": -22.5, "lon": -48}, margin=dict(l=0, r=0, t=0, b=0), height=750)

    return fig


status_individual = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR],
                         url_base_pathname='/editar/status/2/')
status_individual.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='mapa-edicao', figure=plotar_mapa_de_edicao())
        ], sm=6),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.H1(id='cidade-selecionada', className='cidade-selecionada-editar-status')
                ], sm=12)
            ])
        ], sm=6)
    ])
], fluid=True)


@status_individual.callback(
    Output('cidade-selecionada', 'children'),
    Input('mapa-edicao', 'clickData'),
)
def mostrar_nome_da_cidade_selecionado_pelo_mapa(clique):
    engine = create_engine('sqlite:///./database/database.db')
    df = pd.read_sql('SELECT * FROM cidades', con=engine)

    if clique:
        id_da_cidade = clique['points'][0]['location']

        for i in df['id'].values:
            if i == id_da_cidade:
                return df.query(f'id == {i}')['name'].values[0]
    raise PreventUpdate
