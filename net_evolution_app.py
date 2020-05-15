import dash, glob, base64, pickle
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_gif_component as gif
from dash.dependencies import Input, Output, State
from PIL import Image, ImageDraw
from collections import Counter
import igraph as ig
from pathlib import Path

image_filename1 = Path('images/sim0.png')
image_filename2 = Path('images/sim1.png')
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

clickBack = 0
clickForward = 0


firstLaunch = True
layout = None


fp_in = Path("network_dumps/nets.pickle")
nets = list()
with open(fp_in, "rb") as f:
    nets = pickle.load(f)
tot = len(nets) - 1


# app layout
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Network evolution'

modelParam = ["S susceptible", "E exposed ", "I infected", "R recovered", "D dead"]

tab1_content = dbc.Container(
        [
            html.Div(style = {'margin-top': '30px'}),
        dbc.Container(id ="div_evolution", 
        children = [
            
            dbc.Row([
                dbc.Col([
                    html.H1("Network evolution"),
                    html.Hr(),
                    html.Br(),
                ], md = 12),


            ],align="center"),

            dbc.Row(
            [
                dbc.Col([
                    dbc.Button("", id ="invisible_button", style= {'display': 'None'}),
                    dbc.Spinner(html.Div(id="gif_id", children= []), color="primary"),
                    html.Div(style = {'margin-top': '60px'}),
                ], md = 7),

                dbc.Col([
                    html.P('Legend:'),
                    html.Ul(id='my-list', children=[html.Li(i) for i in modelParam])
                    
                ], md = 5),
            ]),
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
                ], md=12),

                ],
            ),
            
            
            dbc.Row(
                [
                dbc.Col([
                    dbc.Label("simulation day:"),
                    html.Div(dcc.Slider(id="day_sim", value = 1, min = 0, max = tot,
                                #step=None,
                                marks={
                                    0: {'label': '0'},
                                    #50: {'label': '50%'},
                                    tot: {'label': str(tot)}
                                },
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
                    html.Br(),
                    dbc.Spinner(html.Div(id='div_spin'), color="primary"),
                    
                    dcc.Graph(id="graph_sim", style= {'display': 'block'}),
                    html.Div(style = {'margin-top': '60px'})
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

        html.Div(style = {'margin-top': '600px'}),
        ]
    ,
    className="mt-3",
)




tab2_content = dbc.Container(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", id="button_click"),
            dcc.Graph(id="graphExample2", style= {'display': 'block'}),
            html.Div(style = {'margin-top': '600px'}),
        ], 
        #style= {'display': 'None'}
)


tab3_content = dbc.Container(
        [
            html.P("This is tab 3!", className="card-text"),
            dbc.Button("Don't click here", id="bu_click"),
            dcc.Graph(id="graphExample3", style= {'display': 'block'}, figure ={
                'data': [
                    {'x': [1], 'y': [1], 'type': 'bar', 'name': 'S', 'marker' : {'color': 'Blue'}},
                    {'x': [1], 'y': [3], 'type': 'bar', 'name': 'E', 'marker' : {'color': 'Orange'}},
                    {'x': [1], 'y': [4], 'type': 'bar', 'name': 'I', 'marker' : {'color': 'Red'}},
                    {'x': [1], 'y': [6], 'type': 'bar', 'name': 'R', 'marker' : {'color': 'Green'}},
                    {'x': [1], 'y': [5], 'type': 'bar', 'name': 'D','marker' : {'color': 'Black'}},
                ],
                'layout': {
                    'title': 'esempio' 
                }
                }),
        ], 
        #style= {'display': 'None'}
)


app.layout = dbc.Container(
    [
        dcc.Tabs([
            dcc.Tab(tab1_content, label="Network evolution", id="tab-0"),
            dcc.Tab(tab2_content, label="Tab Marco", id="tab-1"),
            dcc.Tab(tab3_content, label="Tab Andre e Francesco", id="tab-2"),
        ],

        id="tabs",
        #active_tab="tab-0",
        ),

       #html.Div(id="tab_content", children = [])
    ])


@app.callback([Output("gif_id","children")], [Input("invisible_button", "n_clicks")])
def return_GIF(n_click):
    global firstLaunch
    if firstLaunch == False:
        firstLaunch = True
    
    clickBack = 0
    clickForward = 0
    print("ci sono entrato")
    sim_png = 'assets/simulation.png'
    sim_gif = 'assets/simulation.gif'

    encoded_sim_png = base64.b64encode(open(sim_png, 'rb').read())
    encoded_sim_gif = base64.b64encode(open(sim_gif, 'rb').read())
    return [gif.GifPlayer(
                        gif= 'data:image/gif;base64,{}'.format(encoded_sim_gif.decode()),
                        still= 'data:image/png;base64,{}'.format(encoded_sim_png.decode()),
                        autoplay = True,
                    ),]
    



@app.callback([Output("graphExample2", "figure")], [Input("button_click", "n_clicks")])
def testButton(n_click):
    print("bottone cliccato")
    fig = go.Figure()

    # Constants
    img_width = 600
    img_height = 650
    scale_factor = 0.5

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
)

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source='data:image/png;base64,{}'.format(encoded_image1.decode()))
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    return [fig]


@app.callback([Output("graphExample3", "figure")], [Input("invisible_button", "n_clicks")])
def testButton(n_click):
    #print("cliccato0000000000000 tab3")

    return [{'data': [
                    {'x': [1], 'y': [1], 'type': 'bar', 'name': 'S', 'marker' : {'color': 'Blue'}},
                    {'x': [1], 'y': [3], 'type': 'bar', 'name': 'E', 'marker' : {'color': 'Orange'}},
                    {'x': [1], 'y': [4], 'type': 'bar', 'name': 'I', 'marker' : {'color': 'Red'}},
                    {'x': [1], 'y': [6], 'type': 'bar', 'name': 'R', 'marker' : {'color': 'Green'}},
                    {'x': [1], 'y': [5], 'type': 'bar', 'name': 'D','marker' : {'color': 'Black'}},
                ],
                'layout': {
                    'title': 'esempio tab 3' 
                }
                }
                ]



@app.callback(
    [
        Output('back', 'disabled'),
        Output('forward', 'disabled')
    ],
    
    [   
        Input("day_sim", "value"),
    ],


)
def enable_button(sim_day):
        
    if sim_day == 0:
        return [True, False]
    elif sim_day == tot:
        return [False, True]
    else:
        return [False, False]





@app.callback(Output("day_sim", "value"), [Input("back", "n_clicks"), Input("forward", "n_clicks")], [State("day_sim", "value")])
def update_slider(currentClickBack, currentClickForward, day_sim):
    global clickBack, clickForward

    if currentClickBack is not None and currentClickBack > clickBack:
        clickBack += 1
        return day_sim -1
    elif currentClickForward is not None:
        clickForward+=1
        return day_sim +1
    else:
        return 1



@app.callback([Output("graph_sim", "figure"), Output("div_spin", "children"), Output("img_day1", "figure"), Output("img_day2", "figure"), Output("graphImg1", "figure"), Output("graphImg2", "figure"), Output("day_sim", "max")], [Input("day_sim", "value")])
def update_graph(day):
    global firstLaunch, layout, tot
    
    fp_in = Path("network_dumps/nets.pickle")
    nets = list()
    with open(fp_in, "rb") as f:
        nets = pickle.load(f)
    tot = len(nets) - 1
    G = nets[day]

    
    if firstLaunch:
        layout = G.layout("large")
        firstLaunch = False

    colors = {'S':'#0000ff', 'E':'#ffa300', 'I':'#ff0000', 'D':'#000000', 'R':'#00ff00'}
    vertex_color = [colors[status] for status in G.vs["agent_status"]]
    
    node_text = []


    node_trace_x = []
    node_trace_y = []

    infected = [vertex.index for vertex in G.vs if vertex["agent_status"] == 'I']

    #add a pos attribute to each node
    for node in G.vs:
        node_text.append('State: ' + str(node['agent_status']))
        x, y = layout[node.index]
        node_trace_x += tuple([x])
        node_trace_y += tuple([y])

        


    edge_trace_x = []
    edge_trace_y = []
    edge_trace_x_red = []
    edge_trace_y_red = []


    for edge in G.es:
        x0, y0 = layout[edge.source]
        x1, y1 = layout[edge.target]

        if edge.source in infected or edge.target in infected:
            edge_trace_x_red += tuple([x0, x1, None])
            edge_trace_y_red += tuple([y0, y1, None])
        else:
            edge_trace_x += tuple([x0, x1, None])
            edge_trace_y += tuple([y0, y1, None])
            


    edge_trace_gray = go.Scatter(
        x=edge_trace_x,
        y=edge_trace_y,
        line=dict(width=0.3,color='#888'),
        hoverinfo='none',
        mode='lines')

    edge_trace_red = go.Scatter(
        x=edge_trace_x_red,
        y=edge_trace_y_red,
        line=dict(width=0.7,color='#ff0000'),
        hoverinfo='none',
        mode='lines')


    node_trace = go.Scatter(
        x= node_trace_x,
        y= node_trace_y,
        text= node_text,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            #showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            #colorscale='YlGnBu',
            #reversescale=True,
            color= vertex_color,
            size=20,
            #colorbar=dict(
            #    thickness=15,
            #    title='Node Connections',
            #    xanchor='left',
            #    titleside='right'
            #),  
            line=dict(width=2)))

    
    


    fig = go.Figure(data=[edge_trace_gray, edge_trace_red, node_trace],
                 layout=go.Layout(
                    title='<br>Network Graph day '+ str(day),
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    if day > 0:
        image_filename1 = Path('images/sim' + str(day -1)  + '.png')
        image_filename2 = Path('images/sim' + str(day)  + '.png')
        G_prev = nets[day -1]
        day_prev = day -1
    else:
        image_filename1 = Path('images/sim0.png')
        image_filename2 = Path('images/sim0.png')
        G_prev = nets[0]
        day_prev = 0


    encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())
    encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())
    

    src_image1 = go.Figure()

    # Constants
    img_width = 600
    img_height = 650
    scale_factor = 0.7

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    src_image1.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    src_image1.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    src_image1.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    src_image1.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source='data:image/png;base64,{}'.format(encoded_image1.decode()))
    )

    # Configure other layout
    src_image1.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )


    src_image2 = go.Figure()

    # Constants

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    src_image2.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    src_image2.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    src_image2.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    src_image2.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source='data:image/png;base64,{}'.format(encoded_image2.decode()))
    )

    # Configure other layout
    src_image2.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )


    #file = "network_dumps/network" + str(day) + ".pickle"
    #
    agent_status_report = G.vs["agent_status"]
    report = Counter(agent_status_report)
    s = report["S"]
    e = report["E"]
    i = report["I"]
    r = report["R"]
    d = report["D"]


    current = {
            'data': [
                {'x': [1], 'y': [s], 'type': 'bar', 'name': 'S', 'marker' : {'color': colors['S']}},
                {'x': [1], 'y': [e], 'type': 'bar', 'name': 'E', 'marker' : {'color': colors['E']}},
                {'x': [1], 'y': [i], 'type': 'bar', 'name': 'I', 'marker' : {'color': colors['I']}},
                {'x': [1], 'y': [r], 'type': 'bar', 'name': 'R', 'marker' : {'color': colors['R']}},
                {'x': [1], 'y': [d], 'type': 'bar', 'name': 'D','marker' : {'color': colors['D']}},
            ],
            'layout': {
                'title': 'Population summary at Day ' + str(day)
            }
    }

    
    agent_status_report = G_prev.vs["agent_status"]
    report = Counter(agent_status_report)
    s = report["S"]
    e = report["E"]
    i = report["I"]
    r = report["R"]
    d = report["D"]

    prev = {
            'data': [
                {'x': [1], 'y': [s], 'type': 'bar', 'name': 'S', 'marker' : {'color': colors['S']}},
                {'x': [1], 'y': [e], 'type': 'bar', 'name': 'E', 'marker' : {'color': colors['E']}},
                {'x': [1], 'y': [i], 'type': 'bar', 'name': 'I', 'marker' : {'color': colors['I']}},
                {'x': [1], 'y': [r], 'type': 'bar', 'name': 'R', 'marker' : {'color': colors['R']}},
                {'x': [1], 'y': [d], 'type': 'bar', 'name': 'D','marker' : {'color': colors['D']}},
            ],
            'layout': {
                'title': 'Population summary at Day ' + str(day_prev)
            }
    }

    return [fig, [], src_image1, src_image2, prev, current, tot]


# run app on local server
if __name__ == "__main__":
    app.run_server(debug=True, port=8888)