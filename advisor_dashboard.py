import dash
from dash import Dash, dcc, html, Output, Input
from sqlalchemy import create_engine
import pandas as pd


app = Dash(__name__)

# SQLAlchemy engine with connection pooling
engine = create_engine("sqlite:///university.db", pool_size=5, max_overflow=10)

app.layout = html.Div([
    dcc.Dropdown(id="course-dropdown", options=[]),
    html.Div(id="output")
])

@app.callback(
    Output("output", "children"),
    Input("course-dropdown", "value")
)
def update_output(selected_course):
    with engine.connect() as conn:
        query = "SELECT * FROM Courses"
        df = pd.read_sql(query, conn)
    
    return f"Data Loaded: {len(df)} rows"

#if __name__ == "__main__":
#    app.run_server(debug=True)

app = dash.Dash(__name__)
server = app.server