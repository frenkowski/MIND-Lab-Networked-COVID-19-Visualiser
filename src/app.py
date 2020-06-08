import dash_bootstrap_components as dbc
import dash

# app layout
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Network evolution'

server = app.server