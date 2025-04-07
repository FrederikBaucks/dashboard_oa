import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache
# from callbacks import *
# from components import *



# Initialize the app - incorporate css [dbc.themes.COSMO]#
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, '/assets/style.css',
                                                'https://use.fontawesome.com/releases/v5.8.1/css/all.css'])
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

#server = app.server
app.config.suppress_callback_exceptions = True


























# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)