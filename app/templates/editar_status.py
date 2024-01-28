import dash

from app import app
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

modals_ = []
cidades_ = []
inversores_ = []

i_cidades = 0
i_inversores = 0
i_modals = 0

edit_status = Dash(__name__, url_base_pathname='/editar_status/', server=app, external_stylesheets=[dbc.themes.SOLAR])
edit_status.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Adicionar estado(s) de inversor(es)', className='edit-status-card'),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(id='cards-cidades')
                        ], sm=12)
                    ])
                ]),
                dbc.CardFooter([
                    dbc.Button('Adicionar cidade',
                               id='add-cidade',
                               className='edit-status-add-cidade'
                               , color='dark', outline=False)
                ])
            ], color='dark')
        ], sm=12)
    ]),
    dbc.Row(id='area-dos-modals'),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Configurações ModbusTCP")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Input(placeholder='Database', type='text')
                    ], sm=12)
                ])
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    "Close", id="close", className="ms-auto", n_clicks=0
                )
            ),
        ],
        id="modal-tcp",
        is_open=False,
    ),
])


@edit_status.callback(

    Output('cards-cidades', 'children'),
    Input('add-cidade', 'n_clicks')
)
def adicionar_card_de_cidade(cliques):
    global cidades_, i_cidades
    if dash.ctx.triggered_id == 'add-cidade':
        cidades_.append(
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Input(placeholder='Nova cidade', type='text',
                                              id=f'input-add-cidade-{i_cidades + 1}')
                                ], sm=12)
                            ]),
                        ]),
                        dbc.CardBody([
                            dbc.Row(id=f'cards-inversores-cidade-{i_cidades + 1}')
                        ]),
                        dbc.CardFooter([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button('Adicionar inversor',
                                               id=f'btn-add-inv-{i_cidades + 1}', color='dark', outline=False)
                                ], sm=12)
                            ])
                        ])
                    ])
                ], color='dark')
            ], sm=12),
        )
        i_cidades += 1
    return cidades_


# @edit_status.callback(
#     Output(f'cards-inversores-cidade-{i + 1}', 'children'),
#     Input(f'btn-add-inv', 'n_clicks')
# )
# def adicionar_card_de_inversor(cliques):
#     global inversores_, i_inversores
#     if dash.ctx.triggered_id == f'btn-add-inv-{i + 1}':
#         inversores_.append(
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         dbc.Row([
#                             dbc.Col([
#                                 dbc.Input(
#                                     placeholder='Nome do inversor (número ou letra)',
#                                     type='text',
#                                     id=f'input-nome-inversor-inv-{i_inversores + 1}'
#                                 )
#                             ], sm=12)
#                         ]),
#                         dbc.Row([
#                             dbc.Col([
#                                 dbc.Row([
#                                     dbc.ButtonGroup([
#                                         dbc.Button('Configurações ModbusTCP',
#                                                    id=f'config-tcp-inv-{i_inversores + 1}',
#                                                    className='btn-config-inversor'
#                                                    , color='dark', outline=False),
#                                         dbc.Button('Configurações SQL',
#                                                    id=f'config-sql-inv-{i_inversores + 1}',
#                                                    className='btn-config-inversor'
#                                                    , color='dark', outline=False),
#                                     ])
#                                 ]),
#                             ], sm=12)
#                         ])
#                     ])
#                 ], color='dark')
#             ], sm=6)
#         )
#         i_inversores += 1
#     return inversores_
