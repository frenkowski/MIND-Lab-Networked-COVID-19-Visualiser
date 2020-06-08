import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from src.app import app
from src.layouts import tab1_content, tab2_content
import src.callbacks


# app layout
app.layout = dbc.Container(
    [
        dcc.Tabs([
            dcc.Tab(tab1_content, label="Network evolution", id="tab-0"),
            dcc.Tab(tab2_content, label="Simulations comparison", id="tab-2"),
        ],

        id="tabs",
        
        ),
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)