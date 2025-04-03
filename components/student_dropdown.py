import dash_bootstrap_components as dbc
from  dash_bootstrap_components import Row as R, Col as C
from dash import dcc, html
import pandas as pd
from components.button_style import roundbutton
from components import colors
import figures
from pathlib import Path
from dash import dash_table
import sqlite3

# df = pd.read_csv('data/df.csv')
# modul_data = pd.read_csv('data/Pflichtmodule.csv', sep=';')
# df_stud = pd.read_csv('data/df_stud.csv')
# student_data = pd.read_pickle(r'data/AI_raw.pickle')

conn = sqlite3.connect('university.db')
df_stud = pd.read_sql_query("SELECT student_id, gpa, ability FROM Students", conn)
conn.close()
no_stud_chosen = 'no student yet'
dropdown = html.Div(
    dbc.Card(
        dbc.CardBody(
            R([
                C(  
                    # include student icon here, where the icon size is set relative to the card size.
                    html.Img(src='assets/icons/student.png', style={'height':'40px', 'width':'40px'}),
                    style={"flex-basis": "10%"}                                                    
                ),
                C(  
                    dcc.Dropdown(
                        id='student_dropdown',
                        options=[{'label': i, 'value': i} for i in df_stud['student_id']],
                        value = no_stud_chosen
                    ),
                    # set width of dropdown dynamically to width of card
                    style={"flex-basis": "90%"}  
                )
            ],
            style={"display": "flex"})        
        ), 
        color = colors.bright_grey, 
        style={ 'border-radius':'20px',
                                    "border": "none", 
                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                    "background-color": "#F2F2F7"}
    )
)

dropdown_output = html.Div(dbc.Card(dbc.CardBody(id = 'dd-output-container'), color = colors.bright_grey,style={ 'border-radius':'20px',
                                    "border": "none", 
                                    "box-shadow": "0 5px 8px 0 rgba(0,0,0,0.2)", 
                                    "background-color": "#F2F2F7"}))
