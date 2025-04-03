import dash_bootstrap_components as dbc
from  dash_bootstrap_components import Row as R, Col as C
from dash import dcc, html
import pandas as pd
from components.button_style import roundbutton
from components import colors
import figures
from pathlib import Path
from dash import dash_table

# df = pd.read_csv('data/df.csv')
# modul_data = pd.read_csv('data/Pflichtmodule.csv', sep=';')
# df_stud = pd.read_csv('data/df_stud.csv')
# student_data = pd.read_pickle(r'data/AI_raw.pickle')
# no_stud_chosen = 'no student yet'
work_hist = html.Div(dbc.Card(                                 
                                dbc.CardBody([R([C(html.H4("Distribution of Student Workloads", className="card-title")), 
                                                C(html.Button('?', id='help_button_work', n_clicks=0, style = roundbutton, className="ios-button"), width={'offset':0, "size": 1}),
                                                dcc.ConfirmDialog(id='popup_id_work',
                                                              message=Path('explanations/work.txt').read_text())]), 
                                                dcc.Graph(figure=figures.get_work_fig(), 
                                                          id='work_hist',
                                                          style={'margin':25})])
                                ,
                                  color = colors.bright_grey,
                                  style={ 'border-radius':'15px',
                                    "border": "none", 
                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                    "background-color": "#F2F2F7"}))  