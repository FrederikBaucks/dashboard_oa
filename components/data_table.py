import dash_bootstrap_components as dbc
from  dash_bootstrap_components import Row as R, Col as C
from dash import dcc, html
import pandas as pd
from components.button_style import roundbutton, help_modal, roundbutton_raw_data
from components import colors
import figures
from pathlib import Path
from dash import dash_table
import dash_daq as daq

# df = pd.read_csv('data/df.csv')
# modul_data = pd.read_csv('data/Pflichtmodule.csv', sep=';')
# df_stud = pd.read_csv('data/df_stud.csv')
# student_data = pd.read_pickle(r'data/AI_raw.pickle')
# df_raw = pd.read_csv('data/raw.csv')

table = html.Div(dbc.Card( 
                                dbc.CardBody([R([C(html.H4("Taken Courses", className="card-title")),
                                        C([html.Button('?', id='help_button_data_table', n_clicks=0, style = roundbutton, className="ios-button"),
                                           help_modal]
                                          , width={'offset':0, "size": 1}),
                                        dcc.ConfirmDialog(id='popup_id_data_table', 
                                                              message=Path('explanations/data_table.txt').read_text())]),
                                        html.Div(
                                                dash_table.DataTable(
                                                                data = pd.DataFrame().to_dict('records'), 
                                                                columns = [{"name": i, "id": i} for i in pd.DataFrame().columns], 
                                                                id='student_data_table',
                                                                style_data_conditional=[{'color': 'black'}],
                                                                style_table={'overflowY': 'scroll',
                                                                                'height': '370px'},
                                                                
                                                                sort_action="native",
                                                                sort_mode="multi"),
                                                className='table-container',
                                                ),
                                        dcc.Slider(0, 1, 1,
                                                    marks={
                                                            0: 'all',
                                                            1: 'last semester'
                                                            },
                                                        value=0,
                                                        id='semester-slider')
                                        ],
                                        style={"font-size": "16px", "color": "#000"}),
                            color = colors.bright_grey,
                            style={ 'border-radius':'15px',
                                    'height': '500px',
                                    "border": "none", 
                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                    "background-color": "#F2F2F7"}))


table_raw = html.Div(dbc.Card( 
                                dbc.CardBody([R([C(html.H4("Raw Student Data", className="card-title")),
                                        C([html.Button('?', id='help_button_data_table', n_clicks=0, style = roundbutton_raw_data, className="ios-button"),
                                           help_modal]
                                          , width={'offset':0, "size": 1}),
                                        dcc.ConfirmDialog(id='popup_id_data_table',
                                                              message=Path('explanations/data_table.txt').read_text())]),
                                        html.Div(
                                                dash_table.DataTable(
                                                                data = pd.DataFrame().to_dict('records'), 
                                                                columns = [{"name": i, "id": i} for i in pd.DataFrame().columns], 
                                                                id='student_data_table_raw',
                                                                style_data_conditional=[{'color': 'black'}],
                                                                style_table={'overflowY': 'scroll',
                                                                                'height': '62vh'},
                                                                
                                                                sort_action="native",
                                                                sort_mode="multi"),
                                                className='table-container'
                                                ),
                                        dcc.Slider(0, 1, 1,
                                                    marks={
                                                            0: 'all',
                                                            1: 'last semester'
                                                            },
                                                        value=0,
                                                        id='semester-slider')
                                        ],
                                        style={"font-size": "16px", "color": "#000"}),
                            color = colors.bright_grey,
                            style={ 'border-radius':'15px',
                                    'height': '100%',
                                    "border": "none", 
                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                    "background-color": "#F2F2F7"}))

