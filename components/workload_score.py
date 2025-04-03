import dash_bootstrap_components as dbc
from  dash_bootstrap_components import Row as R, Col as C
from dash import dcc, html
import pandas as pd
from components.button_style import roundbutton
from components import colors
import figures
from pathlib import Path
# from dash import dash_table
import dash_daq as daq

# df =s pd.read_csv('data/df.csv')
# modul_data = pd.read_csv('data/Pflichtmodule.csv', sep=';')
# df_stud = pd.read_csv('data/df_stud.csv')
# student_data = pd.read_pickle(r'data/AI_raw.pickle')

thermometer = dcc.Graph(figure=figures.get_credit_figure(student_mean=0, recom=30, curr=0),
                        id = 'thermometer',
                        style={'height': '230px', "margin-top": "-55px"})





prediction_score = dcc.Graph(figure=figures.get_pred_fig(color=colors.bright_grey, font_color=colors.font_color, mean_stud_perc=0), 
                            id='pred_score',
                            style={'margin':0, 'height': '230px'})

confidence_score = daq.Gauge(
                                id='my-gauge-2',
                                label="Confidence in Prediction",
                                value=6,
                                min=0,
                                max=20
                            ),


choice = html.Div(dbc.Card(dbc.CardBody([R([C(html.H4("Next Semester", className='card-title')),
                                            C(html.Button('?', id='help_button_next_semester', style = roundbutton, className="ios-button"), width={'offset':0, "size": 1}),
                                            dcc.ConfirmDialog(id='popup_id_next_semester',
                                                              message=Path('explanations/next_semester.txt').read_text())]), 
                                                
                                        prediction_score, 
                                        thermometer]),
                            color = colors.bright_grey,
                            style={ 'border-radius':'15px',
                                    'height': '500px',
                                    "border": "none", 
                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                    "background-color": "#F2F2F7"}
                        )
                    )