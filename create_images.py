import igraph as ig
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob, pickle, os
import numpy as np
from pathlib import Path
from matplotlib.collections import LineCollection
from PIL import Image
from pathlib import Path
from collections import Counter



def images_to_gif(name, images):
    """
    Read all simulation images and create GIF. Save the results in "assets" folder
    
    Parameters
    ----------
    name: string
        The name of the result GIF and PNG file

    images: string
        The list of images names
    Return
    ------
    None
    Save the results on file

    """
    imagesList = []
    for image in images:
        imagesList.append(Image.open(image))

    if not os.path.exists("assets"):
            os.mkdir("assets")

    imagesList[0].save(Path('assets/{}_simulation.png'.format(name)))
    imagesList[0].save(Path('assets/{}_simulation.gif'.format(name)), save_all=True, append_images=imagesList[1:], optimize=True, duration=400, loop=0)


def create_dayly_image(nets, day, layout, file_name, save_pdf = False):
    """
    Create the image of the graph in a specific day. The position of the nodes is fixed according to the layout argument. Save the results in "images" folder
    
    Parameters
    ----------
    nets: list of igraph object (graph)
        All the networks of the simulation 
    day: integer
        Current day of simulation

    layout: list of tuple
        Couple of (x, y) position of the node for plotting

    file_name: string
        The name of the result image
    Return
    ------
    None
    Save the results on file

    """
               
    # plot option
    colors = {'S':'#0000ff', 'E':'#ffa300', 'I':'#ff0000', 'D':'#000000', 'R':'#00ff00'}
    node_size = 65
    node_shape = 'o'
    
    # curretn network
    G = nets[day]
    vertex_color = [colors[status] for status in G.vs["agent_status"]]
    edge_color = []

    infected = [vertex.index for vertex in G.vs if vertex["agent_status"] == 'I']
            
    for edge in G.es:
        if edge.source in infected or edge.target in infected:
            edge_color.append('red')
        else:
            edge_color.append('lightgrey')
            

    xy = np.asarray([layout[v] for v in range(len(G.vs))])
            
    edge_pos = np.asarray([(layout[e.source], layout[e.target]) for e in G.es])
            
            
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_visible(False)
    ax.axis('off')
    node_collection = ax.scatter(xy[:, 0], xy[:, 1],
                                     s=node_size,
                                     c = vertex_color
                                     )
            

    ax.tick_params(axis='both',
                   which='both',
                   bottom=False,
                   left=False,
                   labelbottom=False,
                   labelleft=False)

    node_collection.set_zorder(2)

    edge_collection = LineCollection(edge_pos,
                                     colors = edge_color,
                                     linewidths=0.35,
                                     linestyle='solid',
                                    )

    edge_collection.set_zorder(1)  # edges go behind nodes
    ax.add_collection(edge_collection)

    ax.set_title('Day: ' + str(day))


    patch1 = mpatches.Patch(color=colors['S'], label='S')
    patch2 = mpatches.Patch(color=colors['E'], label='E')
    patch3 = mpatches.Patch(color=colors['I'], label='I')
    patch4 = mpatches.Patch(color=colors['R'], label='R')
    patch5 = mpatches.Patch(color=colors['D'], label='D')

    ax.legend(handles=[patch1, patch2, patch3, patch4, patch5], ncol=5, loc='lower center')
    plt.tight_layout()
                

    #save fig
    plt.savefig(file_name, dpi = 100, optimize = True)
    if save_pdf == True:
        plt.savefig(file_name.split(".")[0] + str('pdf'), dpi = 100, optimize = True)
    plt.cla()
    plt.clf()
    plt.close('all')


# read all pickle file anc create images
if __name__ == "__main__":
    files = os.listdir('network_dumps/')

    all_pickles_names = [i for i in files if i.endswith('.pickle')]

    
    for current_pickle_name in all_pickles_names:

        # Status of evry node day by day
        network_history = {}
        nets = list()
        names = []

        current_file_path = Path("network_dumps/{}".format(current_pickle_name))
            
        print("current file", current_file_path)
        with open(current_file_path, "rb") as f:
            dump = pickle.load(f)
            nets = dump['nets']
        
        # the total number of simulation days
        tot = len(nets)
            
        name = current_pickle_name.split(".")[0]

                # create dir
        if not os.path.exists("images"):
            os.mkdir("images")

        # remove old images
        path_images = str(Path("images/{}_sim".format(name)))

        print("path_images: ", path_images)
        toRemove = glob.glob(str(path_images) + "*.jpeg")
        for image in toRemove:
            os.remove(image)


        # load first network and calculate the position of vertices 
        G = nets[0]

        #fix the vertices position
        layout = G.layout("large")
        
        for day in range(0, tot):

            file_name = Path(path_images + str(day) + ".jpeg")
            print("file_name:", file_name)
            
            create_dayly_image(nets, day, layout, file_name, save_pdf = False)

            # add images for the GIF
            names.append(file_name)
            network_history[day] = Counter(nets[day].vs["agent_status"])

            #check early stopping
            if network_history[day]['I'] + network_history[day]['E'] == 0:
                break
            

        # create GIF
        images_to_gif(name, names)

        # save network historys
        with open(Path('assets/network_history_{}.pickle'.format(name)), 'wb') as handle:
            pickle.dump(network_history, handle)

        