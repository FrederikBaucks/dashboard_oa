import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from app import app

#Create text element. This is the text that will be displayed in the app.
notes = html.Div([
    dbc.Row([
        dbc.Col([
            html.H4("Notes", className="card-title")
            ],  
            width=7)
        
        #dbc.Col([
        #    dbc.Button('Save', id='save', n_clicks=0, class_name='ios-button', style={'width': '100%', 
        #                                                                              'height': '80%',
        #                                                                              'text-align': 'top'})
            ]
            )        
    ,
    html.Div([
        dcc.Textarea(id='textarea', style={'width': '100%', 
                                           'height': '100%', 
                                           'border-radius': '20px',
                                           'font-size': '17px',
                                           'font-family': 'Helvetica'}) 
    ],
    style = {'margin-left': '10vh' , 'width': '100%', 'height': '80vh',
                'position': 'right', 'float': 'right',
                "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)",
                "border-radius": "20px"}),    
])
