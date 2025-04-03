import dash_bootstrap_components as dbc
from  dash_bootstrap_components import Row as R, Col as C
from dash import dcc, html
import pandas as pd
from components.button_style import roundbutton
from components import colors
import figures
from pathlib import Path
import sqlite3

# 

df = pd.read_csv('data/df.csv')

# modul_data = pd.read_csv('data/Pflichtmodule.csv', sep=';')
# df_stud = pd.read_csv('data/df_stud.csv')
# student_data = pd.read_pickle(r'data/AI_raw.pickle')


difficulty_figure = html.Div(dbc.Card(dbc.CardBody([R([C(html.H4("Course Difficulties", className="card-title")),
                                                    C(html.Button('?', id='help_button_diff', n_clicks=0, style = roundbutton, className="ios-button"), width={'offset':0, "size": 1}),
                                                    dcc.ConfirmDialog(id='popup_id_diff',
                                                              message=Path('explanations/diff.txt').read_text())]),
                                                    dcc.Graph(figure=figures.get_diff_fig(df), 
                                                              id='difficulty',
                                                              style={'margin':25, "maxHeight": "450px", "minHeight": "450px", "overflow": "scroll"})]),
                                        color = colors.bright_grey,
                                        style={ 'border-radius':'15px',
                                    "border": "none", 
                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                    "background-color": "#F2F2F7"}))