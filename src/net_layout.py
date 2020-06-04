#
# @author : Marco Distrutti
# @email  : m.distrutti@cmapus.unimib.it
#

import requests
import json
from pprint import pprint

import dash

import dash_html_components as html
import dash_core_components as dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, ALL
import igraph as ig

#######################################
# Global configuration
#######################################

#dynamic css classes
colors = ['red', 'blue', 'green', 'brown', 'pink', 'darkorange', 'black', 'darkcyan', 'orange']
shapes = ['triangle', 'rectangle', 'ellipse', 'hexagon', 'diamond']
selected_color = 'navy'

#styling categories data mapping
link_colors = {'family_contacts' : 'brown', 'frequent_contacts' : 'red', 'occasional_contacts': 'blue', 'random_contacts': 'green'}
agent_shapes = { 'S': 'circle', 'E': 'circle', 'I': 'circle', 'R': 'circle', 'D': 'circle' }
agent_bg = {'S':'#0000ff', 'E':'#ffa300', 'I':'#ff0000', 'D':'#000000', 'R':'#00ff00'}
agent_order = ['S', 'E', 'I', 'R', 'D']

public_callback = None

#######################################
# Generate network from Pickle Object 
#######################################

cy_edges = []
def create_network_data(G):
    if G != "Error":
        global cy_edges
        links_types = []
        lines = ""

        nodes = set()
        cy_edges, cy_nodes = [], []

        for edge in G.es:
            lines = lines + str(edge.source) + " " + str(edge.target) + "\n"
        lines = lines[:-1]
        edges = lines.split("\n")

        node_dictionary = {}
        #precache a nodes map for fast access reading
        for node in G.vs:
            node_dictionary[str(node.index)] = {'agent_status': node["agent_status"]}
            cy_nodes.append({
                "data": {"id": node.index},
                "type": "node", "agent": node["agent_status"],
                "order": agent_order.index(node["agent_status"]),
                "classes": node["agent_status"] + " " + agent_shapes[node["agent_status"]]
            });
        
        for edge in edges:
            source, target = edge.split(" ")
            cy_edges.append({  # Add the Edge Node
                'data': {"id": source+''+target, 'source': source, 'target': target},
                "type": "edge",
                "order": 0
                #,
                #'classes': "mind-edge" #link_colors[category]
            })

        cy_nodes.sort(key=lambda x: x["order"], reverse=False)
        return cy_edges + cy_nodes
    else:
        return

def check_element(element, id):
    if(element["type"] == "node" and element["data"]["id"] == id):
        return True
    elif(element["type"] == "edge" and (element["data"]["source"] == id or element["data"]["target"] == id)):
        return True
    return False


#######################################
# Stylesheet base object 
#######################################

default_stylesheet = [
    {
        "selector": "node",
        "style": {
            "border-width": 2
        }
    },
    {
        "selector": 'edge',#'.mind-edge',
        'style': {
            "curve-style": "bezier",
            "opacity": 0.5,
            'width': 1
        }
    },{
        "selector": ':selected',
        'style': {
            'background-color': selected_color
        }
    },
    #dynamic css classes generation
    *[{
        "selector": '.' + agent,
        'style': {'line-color': agent_bg[agent], 'background-color': agent_bg[agent]}
    } for agent in agent_bg],
    #dynamic css classes generation
    *[{
        "selector": '.' + color,
        'style': {'line-color': color, 'background-color': color}
    } for color in colors],
    #'c0000ff', 'cffa300', 'cff0000', 'c000000', 'c00ff00'
    *[{
        "selector": '.' + shape,
        'style': {'shape': shape}
    } for shape in shapes]
]

#######################################
# UI Controls 
#######################################

def NamedDropdown(name, **kwargs):
    return html.Div(
        style={'margin': '10px 0px'},
        children=[
            #html.P(
            #    children=f'{name}:',
            #    style={'margin-left': '3px'}
            #),

            dcc.Dropdown(**kwargs)
        ]
    )

def DropdownOptionsList(*args):
    return [{'label': val.capitalize(), 'value': val} for val in args]

#######################################
# Rendering functions 
#######################################

def Do_html_layout(elements):
    app.layout = Get_Grid_Div(elements)


def Get_Grid_Div(app, id, elements = []):
    global default_stylesheet, public_callback
    htmlDiv = html.Div([
        cyto.Cytoscape(
            id={
                "type": "day",
                "day": id
            },#'cytoscape',
            elements=elements,
            stylesheet=default_stylesheet,
            layout={'name': 'grid'},
            style={'height': '40vh', 'width': '100%'}
        )
    ], id='container')
    if public_callback is None:
        public_callback = register_callback(app)
    return htmlDiv

lastNode = None

#######################################
# Dynamic callback register 
#
# retrieves the dash app from external client and register a callback
#######################################

def register_callback(app):
    @app.callback([Output({"type": 'day', "day": ALL}, 'stylesheet'),
                  Output({"type": 'day', "day": ALL}, 'layout')],
                  [Input({"type": 'day', "day": ALL}, 'tapNodeData'),
                   Input({"type": 'day', "day": ALL}, 'elements'),
                   Input('dropdown-layout', 'value')
                   ])
    def displayTapNodeData(selected, all_elements, layout):
        global lastNode
        user_click = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        stylesheet = default_stylesheet[:] #default_stylesheet copy for a new css rules set
        
        #default configuration for the selected elements
        selectedConfig = {
            "mid-target-arrow-color": 'blue',
            "mid-target-arrow-shape": "vee",
            "line-color": selected_color,
            "background-color": selected_color,
            "opacity": 1,
            "z-index": 5000
        }
        
        #print("ok")
        
        elements = all_elements[0]
        data = selected
        if(isinstance(selected, list)):
            data = selected[0]
        
        if data is None:
            return [[stylesheet], [{"name": layout}]]
        
        #print("OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        #get all the involved edges    
        edges = [edge for edge in elements if(edge["type"] == "edge" and ( edge["data"]["source"] == data["id"] or edge["data"]["target"] == data["id"]))]
        #get all the nodes involved: every node correlated to the extracted edges
        nodes = [node for node in elements if node["type"] == "node" and len(
                    [e for e in edges if node["data"]["id"] == e["data"]["source"] or node["data"]["id"] == e["data"]["target"]]
                ) > 0]

        for node in nodes:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(node["data"]['id']),
                "style": selectedConfig
            })
        for edge in edges:
            stylesheet.append({
                "selector": 'edge[id = "{}"]'.format(edge["data"]["source"]+""+edge["data"]["target"]),
                "style": selectedConfig
            })
            
        if(user_click != 'container'):# and ( )):
            return [[stylesheet], [{"name": layout}]]
        elif(lastNode != None and lastNode == data['id']):
            lastNode = None
            return [[default_stylesheet], [{"name": layout}]]
        
        elements.sort(key=lambda x: x["order"], reverse=False)
        
        lastNode = data['id']
        return [[stylesheet], [{"name": layout}]]
        
    #closure end
    return displayTapNodeData