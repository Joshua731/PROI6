from app import app
from dash import Dash, html, dcc, Output, Input
from app.templates.partials.index import navbar
import dash_bootstrap_components as dbc

# Crie uma instância do aplicativo Dash
alertas_notificacoes = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR],
                            url_base_pathname='/alertas_notificacoes/')

# Layout do corpo da tela
alertas_notificacoes.layout = dbc.Container([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.H1('Alertas e Notificações', className="mb-4 text-center"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Lista de Alertas e Notificações"),
                dbc.CardBody([
                    html.Ul([
                        html.Li('Alerta 1: Descrição do alerta ou notificação.', className="mb-2"),
                        html.Li('Alerta 2: Descrição do alerta ou notificação.', className="mb-2"),
                        html.Li('Alerta 3: Descrição do alerta ou notificação.', className="mb-2")
                    ])
                ])
            ], className="mb-4")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Detalhes do Alerta"),
                dbc.CardBody([
                    html.P('Data e Hora: XX/XX/XXXX XX:XX', className="mb-2"),
                    html.P('Gravidade: Alta', className="mb-2"),
                    html.P('Descrição: Descrição detalhada do alerta ou notificação.', className="mb-2"),
                    dbc.Button('Marcar como Lido', id='marcar-lido-button', color="primary", className="mt-3")
                ])
            ], className="mb-4")
        ], md=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filtrar Alertas"),
                dbc.CardBody([
                    dcc.Dropdown(
                        options=[
                            {'label': 'Gravidade Alta', 'value': 'alta'},
                            {'label': 'Gravidade Média', 'value': 'media'},
                            {'label': 'Gravidade Baixa', 'value': 'baixa'}
                        ],
                        value='alta',
                        className="mb-2"
                    )
                ])
            ], className="mb-4")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Criar Nova Notificação"),
                dbc.CardBody([
                    dcc.Textarea(
                        placeholder='Insira o texto da notificação aqui...',
                        style={'width': '100%'},
                        className="mb-2"
                    ),
                    dbc.Button('Enviar Notificação', id='enviar-notificacao-button', color="primary", className="mt-3")
                ])
            ], className="mb-4")
        ], md=6)
    ])
]
    # className="pt-5"
    , fluid=True)


# Callbacks

# Callback para marcar um alerta como lido
@alertas_notificacoes.callback(
    Output('marcar-lido-button', 'children'),
    [Input('marcar-lido-button', 'n_clicks')]
)
def marcar_alerta_como_lido(n_clicks):
    # Lógica para marcar o alerta como lido
    return "Alerta marcado como lido"


# Callback para enviar uma nova notificação
@alertas_notificacoes.callback(
    Output('enviar-notificacao-button', 'children'),
    [Input('enviar-notificacao-button', 'n_clicks')]
)
def enviar_notificacao(n_clicks):
    # Lógica para enviar uma nova notificação
    return "Notificação enviada com sucesso"


@alertas_notificacoes.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path
