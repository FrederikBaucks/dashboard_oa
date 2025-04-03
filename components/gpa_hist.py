import dash_bootstrap_components as dbc
from  dash_bootstrap_components import Row as R, Col as C
from dash import dcc, html
import pandas as pd
from components.button_style import roundbutton
from components import colors
import figures
from pathlib import Path
import sqlite3

# df = pd.read_csv('data/df.csv')
# modul_data = pd.read_csv('data/Pflichtmodule.csv', sep=';')
# df_stud = pd.read_csv('data/df_stud.csv')
# student_data = pd.read_pickle(r'data/AI_raw.pickle')


conn = sqlite3.connect('university.db')
df_stud = pd.read_sql_query("SELECT student_id, gpa, ability FROM Students", conn)
conn.close()

gpa_hist = html.Div(dbc.Card(                                 
                                dbc.CardBody([R([C(html.H4("Distribution of Student GPAs", className="card-title")), 
                                                C(html.Button('?', id='help_button_gpa', n_clicks=0, style = roundbutton, className="ios-button"), width={'offset':0, "size": 1}),
                                                dcc.ConfirmDialog(id='popup_id_gpa',
                                                              message=Path('explanations/gpa.txt').read_text())]), 
                        
                                                dcc.Graph(figure=figures.get_gpa_fig(df_stud), 
                                                          id='gpa_hist',
                                                          style={'margin':25})])
                                ,
                                  color = colors.bright_grey,
                                  style={ 'border-radius':'15px',
                                    "border": "none", 
                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                    "background-color": "#F2F2F7"}))