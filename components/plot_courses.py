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

planning = html.Div(dbc.Card(dbc.CardBody([R([C(html.H4("Potential Courses", className='card-title')),
                                           C(html.Button('?', id='help_button_pot_courses', style = roundbutton, className="ios-button"), width={'offset':0, "size": 1}),
                                           dcc.ConfirmDialog(id='popup_id_pot_courses',
                                                              message=Path('explanations/pot_courses.txt').read_text())]), 
                                                
                                           dash_table.DataTable(data = pd.DataFrame().to_dict('records'), 
                                                            columns = [{"name": i, "id": i} for i in pd.DataFrame().columns], 
                                                            id='possible_courses',
                                                            style_data_conditional=[{'color': 'black'}],
                                                            style_table={'overflowY': 'scroll',
                                                                         'height': '370px'},
                                                            row_selectable="multi",
                                                            selected_rows=[],
                                                            sort_action="native",
                                                            sort_mode="multi"),
                                            dcc.Slider(0, 2, 1,
                                                    marks={ 0: 'both',
                                                            1: 'summer term',
                                                            2: 'winter term'
                                                            
                                                            },
                                                        value=0,
                                                        id='sum_win_slider')
                                            ]),
                            color = colors.bright_grey,
                            style={ 'border-radius':'15px',
                                    'height': '500px',
                                    "border": "none", 
                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                    "background-color": "#F2F2F7"}))  