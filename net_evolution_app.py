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

save_pdf = False

#import for grid layout
import mind_tracing as mind_tr


# gloabal variables for handle click forward and back button
clickBack = 0
clickForward = 0

# available simulation to visualize
networks_dictionary = {}
networks_dictionary['Baseline'] = "sim_no_restr"
networks_dictionary['sim1'] = 'sim_dump1'
networks_dictionary['sim2'] = "sim_dump2"
networks_dictionary['sim3'] = "sim_dump3"
networks_dictionary['sim4'] = "sim_dump4"
networks_dictionary['sim5'] = "sim_dump5"

# net to load at first launch
current_nets = 'Baseline'

image_filename1 = Path('images/{}_sim0.jpeg'.format(networks_dictionary[current_nets]))
image_filename2 = Path('images/{}_sim1.jpeg'.format(networks_dictionary[current_nets]))
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

#load baseline
fp_in = Path("network_dumps/{}.pickle".format(networks_dictionary[current_nets]))
nets = list()
with open(fp_in, "rb") as f:
    dump = pickle.load(f)
    nets = dump['nets']

# load baseline history
history_path = "assets/network_history_{}.pickle".format(networks_dictionary[current_nets])

with open(history_path, "rb") as f:
    current_network_history = pickle.load(f)

tot = len(current_network_history) - 1

# fix position of nodes for plotting
layout = nets[0].layout("large")

# app layout
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Network evolution'

server = app.server

modelParam = ["Susceptible, nodes that are not yet infected", 
              "Exposed, represents the people that have been infected, but they are not contagious yet", 
              "Infected, nodes that can trasmit the disease to a susceptible individual", 
              "Recovered, people recovered from the disease, these individuals are immune to the infection", 
              "Dead, nodes not survivor at the disease"]

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
                    dbc.Label("Network type:"),
                    dcc.Dropdown(
                        id="network_id",
                        options=[
                            {"label": col, "value": col} for col in networks_dictionary.keys()
                        ],
                        value="Baseline",
                        clearable=False
                    ), 
                ], md = 12),


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

            
            
            html.Br(),
            html.P('Nodes in the network fall into one of five exclusive states:'),
            html.Ul(id='my-list', children=[html.Li(i) for i in modelParam]),
            html.P('We assumed that recoverd individuals do not become susceptible, but enjoy permanent immunity. The total population size was fixed'),
            html.Br(),
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
                    html.Div(style = {'margin-top': '60px'}),
                    
                    #20200518 - Marco Start
                    html.Div(style = {'margin-top': '10px', 'border-top': '1px solid silver'}),
                    html.Br(),
                    html.H3("Grid layout"),
                    mind_tr.NamedDropdown(
                        name = 'Layout',
                        id = 'dropdown-layout',
                        options = mind_tr.DropdownOptionsList(
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
                    html.Div(id="cyto-container", children = [
                        mind_tr.Get_Grid_Div(app, "cyto_1", mind_tr.create_network_data(nets[0])) 
                    ])
                    #20200518 - Marco End
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

        html.Div(style = {'margin-top': '600px'}),
        ]
    ,
    className="mt-3",
)




tab2_content = dbc.Container(
            [
        html.Div(style={'margin-top': '60px'}),
        dbc.Container(id="div_days_tab3",
        children=[
            dbc.Row(
                [
                dbc.Col([
                    html.Br(),
                    html.H3("Evolution day by day"),
                    html.Br(),
                    html.P('Here, you can see the evolution of the net dynamically. You can choose the day throught the slidebar and visualize the relative plot of the situation. You can see also the relative graph. The aim of the lineplot is to show the long term evolution of the network in terms of SEIRD parameters:'),
                    html.Ul(children=[html.Li(i) for i in modelParam]),
                ], md=12),

                ],
            ),


            dbc.Row(
                [
                dbc.Col([
                    dbc.Label("simulation day:"),
                    html.Div(dcc.Slider(id="slider_day_sim_tab2", value=tot, min=0, max=tot,
                                # step=None,
                                marks={
                                    0: {'label': '0'},
                                    # 50: {'label': '50%'},
                                    tot: {'label': str(tot)}
                                },
                                vertical=False,
                                ),
                                style={'width': '100%', 'display': 'block'},
                    ),
                    html.Br(),
                    dbc.Spinner(html.Div(id='div_spin_tab3'), color="primary"),

                    dcc.Graph(id="graph_evolution_sim", style={'display': 'block'}),
                    dcc.Graph(id="simulation_image_tab2", style={'display': 'block'}),
                ], md=12),

                ]),
        ],
        style={'background-color': '#f2f2f2', 'border-radius': '4px', 'box-shadow': '2px 2px 2px lightgrey'},
        ),
        ],
        # style= {'display': 'None'}
)


app.layout = dbc.Container(
    [
        dcc.Tabs([
            dcc.Tab(tab1_content, label="Network evolution", id="tab-0"),
            dcc.Tab(tab2_content, label="Tab2", id="tab-1"),
            #dcc.Tab(tab3_content, label="Tab Andre e Francesco", id="tab-2"),
        ],

        id="tabs",
        
        ),
    ])

# update  page content with the selected network id
@app.callback([Output("gif_id","children"), Output("gif_id_inf","children"), Output("stats", "children"), Output("day_sim", "max"), Output("day_sim", "marks")], [Input("network_id", "value")], [State("day_sim", "value")])
def update_page_content(network_id, day_sim_current_value):
    """
    Update the page content when a new network is selected. This callback update also the slider max value with the new simulation duration.
    
    Parameters
    ----------
    network_id: string
        id of net to load
    
    day_sim_current_value: integer
        Current day of simulation

    Return
    ------
    GIF div with current image.
    Stats div with current statisitcs.
    Max value e marker style of slider in according to new network loaded.

    """

    global current_nets, networks_dictionary, nets, tot, layout, current_network_history
    
    #reload curent network
    file_name = networks_dictionary[network_id]
    
    if current_nets != network_id:
        current_nets = network_id
        
        new_path = Path("network_dumps/{}.pickle".format(file_name))
        nets = list()
        with open(new_path, "rb") as f:
            dump = pickle.load(f)
            nets = dump['nets']
        

        history_path = "assets/network_history_{}.pickle".format(networks_dictionary[current_nets])

        with open(history_path, "rb") as f:
            current_network_history = pickle.load(f)

        tot = len(current_network_history) - 1

        # fixed position of node
        layout = nets[0].layout("large")

    

    # GIF load
    sim_png = Path('assets/{}_simulation.png'.format(file_name))
    sim_gif = Path('assets/{}_simulation.gif'.format(file_name))

    encoded_sim_png = base64.b64encode(open(sim_png, 'rb').read())
    encoded_sim_gif = base64.b64encode(open(sim_gif, 'rb').read())



    GIF = gif.GifPlayer(
            gif= 'data:image/gif;base64,{}'.format(encoded_sim_gif.decode()),
            still= 'data:image/png;base64,{}'.format(encoded_sim_png.decode()),
            autoplay = True,
          )

    sim_png = Path('assets/{}_inf_simulation.png'.format(file_name))
    sim_gif = Path('assets/{}_inf_simulation.gif'.format(file_name))

    encoded_sim_png = base64.b64encode(open(sim_png, 'rb').read())
    encoded_sim_gif = base64.b64encode(open(sim_gif, 'rb').read())
    
    GIF_inf = gif.GifPlayer(
            gif= 'data:image/gif;base64,{}'.format(encoded_sim_gif.decode()),
            still= 'data:image/png;base64,{}'.format(encoded_sim_png.decode()),
            autoplay = True,
          )
    
    # slider components
    marks = {
            0: {'label': '0'},
            tot: {'label': str(tot)}
    }

    # stats div
    tot_infected = 0
    number_of_nodes = len(nets[0].vs)
    tot_infected = number_of_nodes - current_network_history[tot]['S']

    contacts_sum = 0
    for day in range(len(current_network_history)):
        degree = nets[day].degree()
        contacts_sum += sum(degree)/2   #edge are undirected then necessary /2
    
    avg_contacts = int( contacts_sum / (number_of_nodes * tot))


    stats_current_net =  html.Div(children = [
                    html.H3("Simulation summary"),
                    html.P('Number of nodes: ' + str(number_of_nodes)),
                    html.P('Average dayly number of contacts: ' + str(avg_contacts)),
                    html.P('Simulation duration: ' + str(tot)),
                    html.P('Total infected people: ' + str(tot_infected)),
                    html.P('Total dead people: ' + str(current_network_history[tot]['D']))
                    ])
    

    return [GIF, GIF_inf, stats_current_net, tot, marks]
    



@app.callback(
    [Output('back', 'disabled'), Output('forward', 'disabled')],
    [Input("day_sim", "value"),],
)

# check enable button forward and back
def enable__disable_buttons(sim_day):

    """
    Enable or diseable forward and back buttons in according to the current value of the slider.
    
    Parameters
    ----------
    
    sim_day: integer
        Current day of simulation

    Return
    ------
    disabled: list [bool, bool]
        [backDisabled, ForwardDisabled] if True the specif button is disable if True is clickable 

    """
        
    if sim_day == 0:
        return [True, False]
    elif sim_day >= tot:
        return [False, True]
    else:
        return [False, False]





@app.callback(Output("day_sim", "value"), [Input("back", "n_clicks"), Input("forward", "n_clicks")], [State("day_sim", "value")])
def update_slider(currentClickBack, currentClickForward, day_sim):
    """
    Update the slderbar when button forward or back is clicked
    
    Parameters
    ----------
    
    currentClickBack: integer
        Number of click of the back button, use to avoid updating first auto-call e refresh in dash

    currentClickForward: integer
        Number of click of the forward button, use to avoid updating first auto-call e refresh in dash
    
    day_sim: integer
        Current day of simulation

    Return
    ------
    disabled: list [bool, bool]
        [backDisabled, ForwardDisabled] if True the specif button is disable if True is clickable 

    """

    global clickBack, clickForward
    if day_sim >= tot:
        day_sim = tot
    if currentClickBack is not None and currentClickBack > clickBack:
        clickBack += 1
        return day_sim -1
    elif currentClickForward is not None:
        clickForward+=1
        return day_sim +1
    else:
        return 1



@app.callback([Output("graph_sim", "figure"), 
               Output("div_spin", "children"), 
               Output("img_day1", "figure"), 
               Output("img_day2", "figure"), 
               Output("graphImg1", "figure"), 
               Output("graphImg2", "figure"),
               Output('cyto-container', 'children')],  #20200518 - Marco
              [Input("day_sim", "value"), Input("day_sim", "max")])

def update_graphics(day, max_slider):
    """
    Update the slderbar when button forward or back is clicked
    
    Parameters
    ----------
    
    day: integer
        Current day of simulation

    max_slider: integer
        Current max number of day in simulation

    Return
    ------
    outputs: list of all graphics and images to update
        graph_sim plotly interactive figure 
        div_spin use to show spinner loading component
        img_day1 plotly figure to show prev graph situation in a image
        img_day2 plotly figure to show current situation in a image
        graphImg1 plotly figure that show summary of the status of the prev network
        graphImg2 plotly figure that show summary of the status of the current network
        cyto-container Div to plot grid-layout
    """

    global layout, tot, current_nets, networks_dictionary

    file_name = networks_dictionary[current_nets]

    # check extra day in slider
    if day >= max_slider:
        day = max_slider
    
    G = nets[day]

    # plotly graph 
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

    
    # get current and prev images
    if day > 0:
        image_filename1 = Path('images/{}_sim'.format(file_name) + str(day -1)  + '.jpeg')
        image_filename2 = Path('images/{}_sim'.format(file_name) + str(day)  + '.jpeg')
        day_prev = day -1
    else:
        image_filename1 = Path('images/{}_sim0.jpeg'.format(file_name))
        image_filename2 = Path('images/{}_sim0.jpeg'.format(file_name))
        day_prev = 0


    encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())
    encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())
    

    # create graph for display images 
    src_image1 = go.Figure()

    # Constants
    img_width = 600
    img_height = 600
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
    src_image1.layout.update(
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


    
    # graph current summary situation 

    s = current_network_history[day]["S"]
    e = current_network_history[day]["E"]
    i = current_network_history[day]["I"]
    r = current_network_history[day]["R"]
    d = current_network_history[day]["D"]


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

    
    # graph prev summary situation 
    s = current_network_history[day_prev]["S"]
    e = current_network_history[day_prev]["E"]
    i = current_network_history[day_prev]["I"]
    r = current_network_history[day_prev]["R"]
    d = current_network_history[day_prev]["D"]

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

    if save_pdf == True:
        fig.write_image("graph.pdf")
        prevFig = go.Figure(prev)
        prevFig.write_image("prev.pdf")
        currentFig = go.Figure(current)
        currentFig.write_image("current.pdf")

    return [fig, [], src_image1, src_image2, prev, current, mind_tr.Get_Grid_Div(app, "cyto_" + str(day), mind_tr.create_network_data(G))] #20200518 - Marco


#------callback tab2 -------------

# load curretnt image simulation according to slider value 
@app.callback([Output("simulation_image_tab2","figure")], [Input("slider_day_sim_tab2", "value"), Input("day_sim", "max")])
def return_img(slider_day_sim_tab2, new_max):
    global networks_dictionary, current_nets
    """
    Update the simulation image according to slider value 
    
    Parameters
    ----------
    
    slider_day_sim_tab2: integer
        Current day of simulation

    new_max: integer
        Current max number of day in simulation

    Return
    ------
    outputs: simulation_image_tab2 (figure)
        plotly figure that show the simulaton at the current day
    """

    if slider_day_sim_tab2 > new_max:
        slider_day_sim_tab2 = new_max

    RANGE = [0, 1]
    day = int(slider_day_sim_tab2)
    file_name = networks_dictionary[current_nets]
    image_filename = Path('images/{}_sim'.format(file_name) + str(day)  + '.jpeg')

    
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())

    return [{'data':[], 
    'layout': {
                'xaxis': {
                    'range': RANGE,
                    'showgrid':False,
                    'zeroline': False,
                    'showline': False,
                    'ticks': '',
                    'showticklabels': False,
                },
                'yaxis': {
                    'range': RANGE,
                    'scaleanchor': 'x',
                    'scaleratio': 1,
                    'zeroline': False,
                    'showgrid':False,
                   'showline': False,
                                       'ticks': '',
                    'showticklabels': False,
                },
                'height': 600,
                'images': [{
                    'xref': 'x',
                    'yref': 'y',
                    'x': RANGE[0],
                    'y': RANGE[1],
                    'sizex': RANGE[1] - RANGE[0],
                    'sizey': RANGE[1] - RANGE[0],
                    'sizing': 'stretch',
                    'layer': 'below',
                    'source': 'data:image/png;base64,{}'.format(encoded_image.decode())
                }],
                
                
                }
    }
                ]


#show the simulaton until the current simualtion day
@app.callback([Output("graph_evolution_sim", "figure"), Output("slider_day_sim_tab2", "max"), Output("slider_day_sim_tab2", "marks")], [Input("slider_day_sim_tab2", "value"), Input("day_sim", "max")])
def update_plot(day, new_max):
    """
    Update the simulation graph according to slider value 
    
    Parameters
    ----------
    
    day: integer
        Current day of simulation

    new_max: integer
        Current max number of day in simulation

    Return
    ------
    outputs: simulation_image_tab2 (figure)
        plotly figure that show the simulaton until the current simualtion day
    """
    global current_network_history

    if day > tot:
        day = tot

    x_axis = []
    y_S = []
    y_E = []
    y_I = []
    y_R = []
    y_D = []

    for i in range(day):
        x_axis.append(i)
        y_S.append(current_network_history[i]["S"])
        y_E.append(current_network_history[i]["E"])
        y_I.append(current_network_history[i]["I"])
        y_R.append(current_network_history[i]["R"])
        y_D.append(current_network_history[i]["D"])

    graph = {'data': [
                    {'x': x_axis, 'y': y_S, 'type': 'line', 'name': 'S', 'marker' : {'color': '#0000ff'}},
                    {'x': x_axis, 'y': y_E, 'type': 'line', 'name': 'E', 'marker' : {'color': '#ffa300'}},
                    {'x': x_axis, 'y': y_I, 'type': 'line', 'name': 'I', 'marker' : {'color': '#ff0000'}},
                    {'x': x_axis, 'y': y_R, 'type': 'line', 'name': 'R', 'marker' : {'color': '#00ff00'}},
                    {'x': x_axis, 'y': y_D, 'type': 'line', 'name': 'D','marker' : {'color': '#000000'}},
                ],
                'layout': {
                    'title': 'Lineplot associated with the network of the day ' + str(day) 
                }
            }
    
    marks = {
            0: {'label': '0'},
            tot: {'label': str(tot)}
    }

    return [graph, tot, marks]




# run app on local server
if __name__ == "__main__":
    app.run_server(debug=True, port=8888)