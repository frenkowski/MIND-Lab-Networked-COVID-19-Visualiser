import igraph as ig
from PIL import Image
import glob, pickle, cairo, os
from igraph.drawing.text import TextDrawer

from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from pathlib import Path

def get_concat_v(graph_path, legend_path):
    graph = Image.open(graph_path)
    legend = Image.open(legend_path)
    
    graph_with_legend = Image.new('RGB', ((graph.width, graph.height + legend.height)))
    graph_with_legend.paste(graph, (0, 0))
    graph_with_legend.paste(legend, (0, graph.height))
    return graph_with_legend

def images_to_gif(images):
    """
    Read all simulation images and create GIF
    
    Parameters
    ----------
    images: string
        The list of images names
    Return
    ------
    None

    """
    imagesList = []
    for image in images:
        imagesList.append(Image.open(image))

    imagesList[0].save(Path('assets/simulation.png'))
    imagesList[0].save(Path('assets/simulation.gif'), save_all=True, append_images=imagesList[1:], optimize=True, duration=400, loop=0)

if __name__ == "__main__":

    network_history = {}

    #path = input("insert path to network dumps folder: ")
    path = Path("network_dumps")
    
    # pickle file
    fp_in = Path("{}\\nets.pickle".format(str(path)))
    nets = list()
    with open(fp_in, "rb") as f:
        nets = pickle.load(f)

    # the total number of simulation days
    tot = len(nets)
    names = []
    
    path_images = str(Path("images/sim"))
    toRemove = glob.glob(str(path_images) + "*.png")
    for image in toRemove:
        os.remove(image)

    # load first network and calculate the position of vertices 
    G = nets[0]

    #fix the vertices position
    layout = G.layout("large")
    colors = {'S':'#0000ff', 'E':'#ffa300', 'I':'#ff0000', 'D':'#000000', 'R':'#00ff00'}
    vertex_color = [colors[status] for status in G.vs["agent_status"]]

    
    
    #create images day by day
    for day in range(0, tot):
        #my_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 600, 650, background="white")

        plot = ig.Plot("plot.png", bbox=(600, 650), background="white")
        
        
        
        file_name = Path(path_images + str(day) + ".png")
        print("Day: ", day)
        

        G = nets[day]
        vertex_color = [colors[status] for status in G.vs["agent_status"]]

        
        edge_color = []
        bbox=(20, 70, 580, 630)
        infected = [vertex.index for vertex in G.vs if vertex["agent_status"] == 'I']


        for edge in G.es:
            if edge.source in infected or edge.target in infected:
                edge_color.append('red')
            else:
                edge_color.append('lightgrey')

        
        plot.add(G, bbox = bbox, vertex_color = vertex_color, edge_color = edge_color, edge_width=0.3, layout = layout)
        
        plot.redraw()

        # Grab the surface, construct a drawing context and a TextDrawer
        ctx = cairo.Context(plot.surface)
        ctx.set_font_size(36)
        drawer = TextDrawer(ctx, "Day " + str(day), halign=TextDrawer.CENTER)
        drawer.draw_at(0, 40, width=600)
        
        #save fig without legend
        plot.save(file_name)

        # add legend and save
        fig_with_legend = get_concat_v(file_name, Path("images/legend.png"))
        fig_with_legend.save(file_name)
        
        
        network_history[day] = Counter(G.vs["agent_status"])
        
        
        
        names.append(file_name)
    

    #create GIF
    images_to_gif(names)

    with open(Path('assets/network_history.pickle'), 'wb') as handle:
        pickle.dump(network_history, handle)
