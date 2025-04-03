import dash_bootstrap_components as dbc
from  dash_bootstrap_components import Row as R, Col as C
from dash import dcc, html
import pandas as pd
from components.button_style import roundbutton, help_modal
#from components import colors
#import figures
#from pathlib import Path
#from dash import dash_table
#import dash_daq as daq
#from app import app
#import networkx as nx
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# df = pd.read_csv('data/df.csv')
# modul_data = pd.read_csv('data/Pflichtmodule.csv', sep=';')
# df_stud = pd.read_csv('data/df_stud.csv')
# student_data = pd.read_pickle(r'data/AI_raw.pickle')
# df_raw = pd.read_csv('data/raw.csv')



# personal_info = dbc.Card(
#                             [
#                                 dbc.CardBody(
#                                     [
#                                         html.H4("Personal Information", className="card-title"),
#                                         #html.P(
#                                          #   [
#                                          #       html.B("Name: "), "Student Name", html.Br(),
#                                          #       html.B("Address: "), "Student Address", html.Br(),
#                                         #        html.B("Student ID: "), "123456789", html.Br(),
#                                         #        html.B("Major: "), "Computer Science", html.Br(),
#                                         #        html.B("Year of Study: "), "3",
#                                          #   ], id='personal_info'
#                                         #),
#                                         dbc.Table(
#                                             [
#                                                 html.Tbody(
#                                                     [
#                                                         html.Tr([html.Td("Name:"), html.Td("None")]),
#                                                         html.Tr([html.Td("Address:"), html.Td("None")]),
#                                                         html.Tr([html.Td("Student ID:"), html.Td("None")]),
#                                                         html.Tr([html.Td("Year of Study:"), html.Td("None")]),
#                                                     ]
#                                                 )
#                                             ],
#                                             bordered=True,
#                                             dark=False,
#                                             hover=True,
#                                             responsive=False,
#                                             striped=True,
#                                             id='personal_info'
#                                         ),
#                                     ]
#                                 ),
#                             ],
#                             #style={"width": "18rem"},
#                         )
personal_info_table = dbc.Table(
    id='personal_info_table',
    bordered=True,
    dark=False,
    hover=True,
    responsive=False,
    striped=True,
)

personal_info = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Personal Information", className="card-title"),
                personal_info_table,
            ]
        ),
    ],
    style={'border-radius': '20px',
           "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)"},
)


academic_history_table = dbc.Table(
    id='academic_history_table',
    bordered=True,
    dark=False,
    hover=True,
    responsive=False,
    striped=True,
)

academic_history = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Academic History", className="card-title"),
                academic_history_table,
            ]
        ),
    ],
    style={'border-radius': '20px',
           "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)"},
)



# academic_history = dbc.Card(
#                             [
#                                 dbc.CardBody(
#                                     [
#                                         html.H4("Academic History", className="card-title"),
#                                         dbc.Table(
#                                             [
#                                                 html.Tbody(
#                                                     [
#                                                         html.Tr([html.Td("Average Grade:"), html.Td("1.3")]),
#                                                         html.Tr([html.Td("Number of Semesters:"), html.Td("6")]),
#                                                         html.Tr([html.Td("ECTS:"), html.Td("180")]),
#                                                         html.Tr([html.Td("ECTS per Semester:"), html.Td("30")]),
#                                                     ]
#                                                 )
#                                             ],
#                                             bordered=True,
#                                             dark=False,
#                                             hover=True,
#                                             responsive=False,
#                                             striped=True,
#                                             id='academic_history'
#                                         ),
                                        
                                    
#                                     ]
#                                 ),
#                             ],
#                             style={"height": "18rem"},
#                         )


recent_courses = dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Recent Courses", className="card-title"),
                                        html.Div(
                                            [
                                                html.Img(src='assets/graph.png', style={'width':'30%'}, id='recent_courses'),
                                            ],
                                            style={'textAlign': 'center'}  # center alignment
                                        )
                                    ]
                                ),
                            ],
                            #style={"width": "18rem"},
                        )
