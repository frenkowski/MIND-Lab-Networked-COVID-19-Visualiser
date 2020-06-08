import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

#import for grid layout
import src.net_layout as net_layout

modelParam = ["Susceptible, nodes that are not yet infected", 
              "Exposed, represents the people that have been infected, but they are not contagious yet", 
              "Infected, nodes that can trasmit the disease to a susceptible individual", 
              "Recovered, people recovered from the disease, these individuals are immune to the infection", 
              "Dead, nodes not survivor at the disease"]

gitlink = "https://gitlab.com/migliouni/ctns_visualizer"

tab1_content = dbc.Container(
        [
        html.Div(style = {'margin-top': '30px'}),
        dbc.Container(id ="div_evolution", 
        children = [
            
            dbc.Row([
                dbc.Col([
                    html.H1("Network evolution"),
                    dbc.Alert(
                        [
                            "This is a light version only for demo. Full code without limitation is available at:  ",
                            html.A("here clikkabile", href=gitlink, className="alert-link"),
                        ],
                        color="warning",
                    ),
                    html.Hr(),
                    html.Br(),
                    html.P('Nodes in the network fall into one of five exclusive states:'),
                    html.Ul(id='my-list', children=[html.Li(i) for i in modelParam]),
                    html.P('We assumed that recoverd individuals do not become susceptible, but enjoy permanent immunity. The total population size was fixed'),
                    html.Br(),
                    html.Div(id ='read_alert', children = []),
                    html.Div(id ='noFiles', children = []),
                    dbc.Label("Network type:"),
                    dbc.Row([dbc.Col([
                                dcc.Dropdown(
                                id="network_id",
                                #options=[
                                #    {"label": col, "value": col} for col in networks_dictionary.keys()
                                #],
                                #value= current_nets,
                                clearable=False
                            ),]), 
                            dbc.Col([dbc.Button("Refresh", id= "refresh")]),
                            ]),
                            
                ], md = 12),
                html.Br(),
                


            ],align="center"),

        
            html.Br(),
            dbc.Row(
            [
                dbc.Col([
                    dbc.Spinner(html.Div(id="gif_id", children= []), color="primary"),
                    html.Div(style = {'margin-top': '60px'}),
                ], md = 6),

                dbc.Col([
                    dbc.Spinner(html.Div(id="gif_id_inf", children= []), color="primary"),
                ], md = 6),
            ]),

            html.Div(id="stats", children = []),

        ], style = {'background-color': '#f2f2f2', 'border-radius': '4px', 'box-shadow': '2px 2px 2px lightgrey'}),

        
        html.Div(style = {'margin-top': '60px'}),
        dbc.Container(id ="div_days", 
        children = [
            dbc.Row(
                [
                dbc.Col([
                    html.Br(),
                    html.H3("Evolution day by day"),
                    html.Br(),
                    html.P('This figure shows the evolution of the network day by day. It is possible to set the day using the slidebar below. alternatively, it is possible to go back or to go ahead using the buttons. Here, you can visualize two different plots:'),
                    html.Ul(children=[
                        html.Li('The visualization of the network graph with the classic representation'),
                        html.Li('The visualization of the network graph with a grid layout representation'),
                        
                        ]),
                ], md=12),

                ],
            ),
            
            
            dbc.Row(
                [
                dbc.Col([
                    dbc.Label("simulation day:"),
                    html.Div(dcc.Slider(id="day_sim", min = 0 ,
                                #step=None,
                                #marks={
                                #    0: {'label': '0'},
                                #},
                                vertical = False,
                                ),
                                style={'width': '100%','display': 'block'},
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                        dbc.Col([ dbc.Button("<--- Back ", id= "back")], width={"offset": 5}),
                        dbc.Col([ dbc.Button("Forward --->", id= "forward")],) #width={"size":3})

                    ]),
                    
                    # hide input to contain data for update slider
                    dbc.Input(id = "div_back",
                        type="number",
                        value= 0,
                        style = {'display':'None'}
                    ),

                    dbc.Input(id = "div_forward",
                        type="number",
                        value= 0,
                        style = {'display':'None'}
                    ),    

                    html.Br(),
                    dbc.Spinner(html.Div(id='div_spin'), color="primary"),
                    
                    dcc.Graph(id="graph_sim", style= {'display': 'block'}),
                    html.Div(style = {'margin-top': '60px'}),
                    
                    
                    html.Div(style = {'margin-top': '10px', 'border-top': '1px solid silver'}),
                    html.Br(),
                    html.H3("Grid layout"),
                    net_layout.NamedDropdown(
                        name = 'Layout',
                        id = 'dropdown-layout',
                        options = net_layout.DropdownOptionsList(
                            #'random',
                            'grid',
                            #'circle',
                            'concentric',
                            #'breadthfirst',
                            #'cose'
                        ),
                        value = 'grid',
                        clearable = False
                    ),
                    html.Div(id="cyto-container", 
                    children = [])
                    
                ], md=12),
            
                ]),
        ],
        style = {'background-color': '#f2f2f2', 'border-radius': '4px', 'box-shadow': '2px 2px 2px lightgrey'}, 
        ),

        html.Div(style = {'margin-top': '60px'}),
        dbc.Container(id ="div_2day",  children = [
        dbc.Row(
                [
                dbc.Col([
                    html.Br(),
                    html.H3("Before and Current"),
                    html.Br(),
                    html.P('These plots change dynamically according to the day defined on the previous slidebar. In particular, this tab shows the differences between the current day setted on the slidebar, with the previous day. This tab provide us a tool to better understand the short term evolution of the network  '),
                ], md=12),

                ],
            ),
        html.Br(),
        dbc.Row([
            dbc.Col([dbc.Spinner(dcc.Graph(id = 'img_day1', style= {'display': 'block'}), color="primary"), html.Br()], md=6),
            dbc.Col([dbc.Spinner(dcc.Graph(id = 'img_day2', style= {'display': 'block'}), color="primary"), html.Br()], md=6),
            html.Div(style = {'margin-top': '80px'}),

        ]),

        dbc.Row([   
                    html.Br(),
                    dbc.Col([dbc.Spinner(dcc.Graph(id="graphImg1", style= {'display': 'block'}), color="primary"), html.Br()], md=6),
                    dbc.Col([dbc.Spinner(dcc.Graph(id="graphImg2", style= {'display': 'block'}), color="primary"), html.Br()], md=6),
            
                ],
                align="center"),
        
        ],
        style = {'background-color': '#f2f2f2', 'border-radius': '4px', 'box-shadow': '2px 2px 2px lightgrey'}, 
        ),

        html.Div(style={'margin-top': '60px'}),
        dbc.Container(id="div_days_tab3",
        children=[
            dbc.Row(
                [
                dbc.Col([
                    html.Br(),
                    html.H3("Evolution day by day"),
                    html.Br(),
                    html.P('Here, you can see the evolution of the net dynamically. You can choose the day throught the slidebar and visualize the relative plot of the situation. You can see also the relative graph. The aim of the lineplot is to show the long term evolution of the network in terms of SEIRD classes'),
                ], md=12),

                ],
            ),


            dbc.Row(
                [
                dbc.Col([
                    dbc.Label("simulation day:"),
                    html.Div(dcc.Slider(id="slider_day_sim_trend", min = 0,
                                # step=None,
                                #marks={
                                #    0: {'label': '0'},
                                #},
                                vertical=False,
                                ),
                                style={'width': '100%', 'display': 'block'},
                    ),
                    html.Br(),
                    dbc.Spinner(html.Div(id='div_spin_tab3'), color="primary"),

                    dcc.Graph(id="graph_evolution_sim", style={'display': 'block'}),
                    dcc.Graph(id="simulation_image_trend", style={'display': 'block'}),
                ], md=12),
                html.Div(style={'margin-top': '600px'}), 
                ]),
              
        ],
        style={'background-color': '#f2f2f2', 'border-radius': '4px', 'box-shadow': '2px 2px 2px lightgrey'},
        ),
        ]
    ,
    className="mt-3",
)



tab2_content = dbc.Container([
        html.H1("Analysis simulation results"),
        dbc.Alert(
                        [
                            "This is a light version only for demo. Full code without limitation is available at:  ",
                            html.A("here clikkabile", href=gitlink, className="alert-link"),
                        ],
                        color="warning",
                    ),
        html.Hr(),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Click and Select Files', href="#")
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
   
    html.Br(),
    html.Div(id ='alert_div'),
    html.Div(id='output-data-upload'),
    html.H2("Uploaded file List"),
    html.Ul(id="file-list"),
    html.Br(),
    html.Div(id='table_parameters'),
    html.Br(),
    html.Div(id='table_parameters2'),
    html.Br(),
    html.Div(id='table_parameters3'),
    html.Br(),
    dbc.Row(children = [
        dbc.Col(dbc.Spinner(dcc.Graph(id="heatMap", style= {'display': 'block'}), color="primary"), width = 12)
    ]),
    html.Br(),
    dbc.Row(children = [
        dbc.Col(dbc.Spinner(dcc.Graph(id="graph_comparison_inf", style= {'display': 'block'}), color="primary"), width = 6),
        dbc.Col(dbc.Spinner(dcc.Graph(id="graph_comparison_dead", style= {'display': 'block'}), color="primary"), width = 6),
    ]),
    html.Br(),
    dbc.Row(children = [
        dbc.Col(dbc.Spinner(dcc.Graph(id="graph_comparison_total_inf", style= {'display': 'block'}), color="primary"), md=6),
        dbc.Col(dbc.Spinner(dcc.Graph(id="graph_simulation_len", style= {'display': 'block'}), color="primary"), md=6),

    ]),
    html.Br(),
    dbc.Row(children = [
        dbc.Col(dbc.Spinner(dcc.Graph(id="scatter_dead", style= {'display': 'block'}), color="primary"), width = 12),
    ]),
    html.Br(),
    dbc.Row(children = [
        dbc.Col(dbc.Spinner(dcc.Graph(id="stack_bar", style= {'display': 'block'}), color="primary"), width = 8)
    ]),
])