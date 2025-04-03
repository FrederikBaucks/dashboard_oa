from dash import dcc, html, dash_table
from dash.dash_table.Format import Group

from app import app
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from  dash_bootstrap_components import Row as R, Col as C
# import everything from the components folder without having to specify the path:
from components.title import title
# from components.ability_hist import ability_hist
from components.colors import dark_grey, bright_grey, font_color
#from components.difficulty_figure import difficulty_figure
from components.gpa_hist import gpa_hist
from components.plot_courses import planning
from components.student_dropdown import dropdown, dropdown_output
from components.work_hist import work_hist
from components.workload_score import choice
from components.data_table import table, table_raw
from components.notes import notes 
from components.personal_info import personal_info, academic_history, recent_courses
#from components.performance import performance
#from components.course_load import course_load
#from components.progress import progress
#from components.performance_quantile import performance_quantile
import dash
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import plotly.graph_objects as go
#from callbacks import *
# App layout



# Define the layout
app.layout = html.Div([
    dbc.Row([ 
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        # Sidebar
                        dbc.Col(title,width=10, style={"font-size": "20", "color": "#000"}
                        ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dropdown
                        ]
                        , width=6),
                        dbc.Col([
                            dbc.Button('Overview', id='btn-overview', color='primary', className='ios-button', n_clicks=0,
                                    style = {'width': '100%', 'height': '100%', 
                                                'position': 'right', 'float': 'right'}),
                        ], 
                        width=2,
                        ),
                        dbc.Col([
                            dbc.Button('Analytics', id='btn-analytics', color='primary', className='ios-button', n_clicks=0, 
                                    style = {'width': '100%', 'height': '100%'})
                        ],
                        width=2,
                        ),
                        dbc.Col([
                            dbc.Button('Raw Data', id='btn-raw', color='primary', className='ios-button', n_clicks=0,
                                    style = {'margin-left': '10vh' , 'width': '100%', 'height': '100%', 
                                                'position': 'right', 'float': 'right'}),
                        ], 
                        width=2,
                        ),
                        #dbc.Col([
                        #    dbc.Button('Notes', id='btn-notes', color='primary', className='ios-button', n_clicks=0,
                        #            style = {'margin-left': '10vh' , 'width': '100%', 'height': '100%', 
                        #                        'position': 'right', 'float': 'right'}),
                        #], 
                        #width=2,
                        #),
                    ]),
                ]),
                color = "#c9cad4", 
                style = {'border-radius' : '20px', 
                        'margin-bottom': '0.5%', 
                        'margin-left': '1%', 
                        'margin-top': '1%'}
                ),
            html.Br(),
            dbc.Row([
                # Main content area
                dbc.Col([
                    html.Div(id='main-content'),
                ], width=12,
                style = {'height' : '100%'}),
            ], 
            style = {'border-radius' : '20px',
                        'margin-bottom': '0.5%', 
                        'margin-left': '0.5%', 
                        #'margin-top': '1%'
                        }
            ),
        ], width=10),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            notes,
                        ], width=12),
                    ]),
                ]),
                color = "#F2F2F7",
                style = {'border-radius' : '20px',
                        #'margin-bottom': '0.5%',
                        #'margin-left': '1.5%',
                        #'margin-top': '1%',
                        'height' : '100%'}
            ),
        ], width=2,
        style = {#'height' : '100%',
                 'margin-top': '1%',
                 'margin-bottom': '0.5%',
                 'margin-right': '0.%'}),
    ]),
])


from course_matrix import net_graph


@app.callback(
    Output('main-content', 'children'),
    [Input('btn-analytics', 'n_clicks'), Input('btn-raw', 'n_clicks'), Input('btn-overview', 'n_clicks')]
)
def update_content(n1, n2, n3):

    # layout_overview =html.Div([dbc.Card(dbc.CardBody([
    #                         #R(  [C(title,width=12, style={"font-size": "26px", "color": "#000"})]                                          , align='center' ), #title
    #                         #html.Br(),
    #                         #R(  [C(dropdown, width=8), C(dropdown_output, width=4)]         , align='center'), #dropdown 
    #                         #html.Br(),
    #                         R(  [C(personal_info, width=6), C(academic_history, width=6)]             , 
    #                         align='center'), #data
    #                         html.Br(),      
    #                         R(  [C( html.Img(id='network-graph', src="assets/graph.png"), width=12)],
    #                         #R(  [C( recent_courses, width=12)],
    #                         align='top'), #figures
    #                     ]), color = "#F2F2F7", style = {'border-radius' : '20px', 'top-margin': '10%', 'height' : '100%'})])

    layout_overview = html.Div([
                                dbc.Card(
                                    dbc.CardBody([
                                        R([C(personal_info, width=6), C(academic_history, width=6)], align='center'), 
                                        html.Br(),
                                        R([C(
                                            
                                            html.Div(
                                                [ 

                                                html.H4("   Degree Overview", className="card-title"),   
                                                dcc.Graph(id='network-graph', figure = net_graph())
                                                ],
                                                style={
                                                    'border-radius': '20px', 
                                                    'border': '1px',
                                                    'background': 'White',
                                                    'padding': '10px',
                                                    'height': '100%',
                                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                                    "background-color": "White"
                                                }
                                            ), 
                                            width=12
                                        )], align='top')
                                    ]),
                                    color="#F2F2F7",
                                    style={'border-radius': '20px', 'top-margin': '10%', 'height': '100%', 'bgcolor': 'White'}
                                )
                            ])


    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-analytics':
            
            layout1 = html.Div([dbc.Card(dbc.CardBody([
                        #R(  [C(title,width=12, style={"font-size": "26px", "color": "#000"})]                                          , align='center' ), #title
                        #html.Br(),
                        #R(  [C(dropdown, width=8), C(dropdown_output, width=4)]         , align='center'), #dropdown 
                        #html.Br(),
                        R(  [C(table, width=4), C(planning, width=4),  C(choice, width=4)]             , 
                          align='center'), #data
                        html.Br(),      
                        R(  [C(None, width=4), C(gpa_hist, width=4), C(work_hist, width=4)]    , 
                          align='top'), #figures
                    ]), color = "#F2F2F7", style = {'border-radius' : '20px', 'top-margin': '0%', 'height' : '100%'})])


            return layout1  # Add your Plotly charts here
        elif button_id == 'btn-raw':
            # Show raw data in a table 
            layout2 = html.Div([dbc.Card(dbc.CardBody([
                        #R(  [C(title,width=12, style={"font-size": "26px", "color": "#000"})]                                          , align='center' ), #title
                        #html.Br(),
                        #R(  [C(dropdown, width=8), C(dropdown_output, width=4)]         , align='center'), #dropdown 
                        #html.Br(),
                        R(  [C(table_raw, width=12, style={'height' : '100%'})]             , align='top', style={'height' : '100%'}) # data
                        ]), color = "#F2F2F7", style = {'border-radius' : '20px', 'top-margin': '0%', 'height' : '100%'})])

            return layout2  # Add your data table here
        elif button_id == 'btn-overview':
            return layout_overview
        else:
            return layout_overview  # Add your data table here
    else:
        return layout_overview
        

if __name__ == '__main__':
    app.run_server(debug=True)