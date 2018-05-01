import igraph as ig
import plotly.offline as py
from plotly.graph_objs import *
from colorhash import ColorHash
from copra_lpa import *
import time

vertex_index = {}


def convert_vertex(v):
    if type(v) is int:
        reverse_index = dict((v, k) for k, v in vertex_index.iteritems())
        return reverse_index[v]
    return vertex_index[v]


def process_file(filename):
    """
    Process an input file for its vertices, edges, and weights.
    :param filename: Name of file to process.
    :return: List of vertices, edges, and weights parsed from the file.
    """

    def parse_line_vertices(ln_list):
        """
        Parse list of vertices from input file into a list.
        :param ln_list: List of lines in input file.
        :return: List of vertices in graph.
        """
        vertex_map = {}
        edge_list = []
        val_count = 1
        for ln in ln_list:
            parts = ln.split()
            src = parts[0]
            dst = parts[1]
            if src not in vertex_map:
                vertex_map[src] = val_count
                val_count = val_count + 1
            if dst not in vertex_map:
                vertex_map[dst] = val_count
                val_count = val_count + 1
            edge_list.append((src, dst))
        global vertex_index
        vertex_index = vertex_map
        return vertex_map.keys()

    def parse_line_edges(ln_list):
        """
        Parse list of edges from file into a list.
        :param ln_list: List of lines in input file.
        :return: List of edges in graph.
        """
        edge_list = []
        for ln in ln_list:
            parts = ln.split()
            src = convert_vertex(parts[0])
            dst = convert_vertex(parts[1])
            edge_list.append((src, dst))
        return edge_list

    def parse_weights(ln_list):
        """
        Parse weights of each line into a list.
        :param ln_list: Igraph graph object to make weighted.
        :return:
        """
        weights = []
        for ln in ln_list:
            weights.append(ln.split()[2])
        return weights

    edge_file = open(filename)
    line_list = edge_file.readlines()
    edge_file.close()
    proc_vertices = parse_line_vertices(line_list)
    proc_edges = parse_line_edges(line_list)
    proc_weights = parse_weights(line_list)
    print(str(len(proc_vertices)) + ' vertices')
    print(str(len(proc_edges)) + ' edges')
    return proc_vertices, proc_edges, proc_weights


def plot_data(vertices, edges, weights, f_name, cscale=0):
    """
    Plot network data in three-dimensional space.
    :param vertices: List of vertices in the network.
    :param edges: List of connections in the network.
    :param f_name: Name of HTML file to generate.
    :param cscale: Color scale for network, blue by default. [(0, Blue), (1, Green), (2, Orange)]
    """
    graph = ig.Graph(edges, directed=False)
    graph.es["weight"] = [weights[e] for e in range(len(graph.es))]

    # calculate_edge_betweenness(graph, weights)

    def build_colorscale(c, vert_list):
        """
        Build the colorscale for vertices in the visualization.
        :param c: Parameter to decide colorscale.
        :param vert_list: List of vertices to color.
        :return: List of colors to associate with each vertex.
        """
        clrs = []
        for v in vert_list:
            q = ColorHash(v)
            col_str = 'rgb('
            if c is 0:
                col_str += '%s,%s,255)' % (q.rgb[0], q.rgb[1])
            elif c is 1:
                col_str += '%s,255,%s)' % (q.rgb[0], q.rgb[2])
            elif c is 2:
                col_str += '255,%s,%s)' % (q.rgb[1], q.rgb[2])
            else:
                col_str += '%s,%s,%s)' % tuple(c.rgb)
            clrs.append(col_str)
        return clrs

    colors = build_colorscale(cscale, vertices)

    # Spatial layout of graph components
    spatial = graph.layout('kk', dim=3)

    def trace_edges(edge_list, layt):
        """
        Build the plot.ly trace to map edges on three-dimensional plane.
        :param edge_list: List of edges to draw.
        :param layt: Three-dimensional layout for visualization.
        :return: Edge trace for plot.ly visualization.
        """
        x_edge, y_edge, z_edge = ([] for i in range(3))
        for e in edge_list:
            x_edge += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
            y_edge += [layt[e[0]][1], layt[e[1]][1], None]  # y-coordinates of edge ends
            z_edge += [layt[e[0]][2], layt[e[1]][2], None]  # z-coordinates of edge ends

        edge_trace = Scatter3d(x=x_edge, y=y_edge, z=z_edge,
                               mode='lines',
                               line=Line(color='rgb(0,0,0)', width=1),
                               hoverinfo='none')
        return edge_trace

    def trace_vertices(vertex_list, layt):
        """
        Build the plot.ly trace to map vertices on three-dimensional plane.
        :param vertex_list: List of vertices to place.
        :param layt: Three-dimensional layout for visualization.
        :return: Vertex trace for plot.ly visualization.
        """
        vertex_trace = Scatter3d(x=[layt[k][0] for k in range(len(vertex_list))],  # x-coordinates of nodes
                                 y=[layt[k][1] for k in range(len(vertex_list))],  # y-coordinates of nodes
                                 z=[layt[k][2] for k in range(len(vertex_list))],  # z-coordinates of nodes
                                 mode='markers', name='cortical areas',
                                 marker=Marker(symbol='dot', size=9, color=colors,
                                               line=Line(color='rgb(50,50,50)', width=0.5)),
                                 text=vertex_list, hoverinfo='text')
        return vertex_trace

    def build_layout():
        """
        Build the plot.ly layout object for the visualization.
        :return: Plot.ly layout object.
        """
        axis = dict(showbackground=False, showline=False, zeroline=False,
                    showgrid=False, showticklabels=False, title='')

        layout = Layout(title="3D visualization of a " + f_name + " cortical area network",
                        showlegend=False,
                        scene=Scene(xaxis=XAxis(axis), yaxis=YAxis(axis), zaxis=ZAxis(axis), ),
                        margin=Margin(t=100),
                        hovermode='closest')
        return layout

    data = Data([trace_edges(edges, spatial),
                 trace_vertices(vertices, spatial)])
    fig = Figure(data=data, layout=build_layout())
    py.plot(fig, filename='output/' + f_name + '.html')


def calculate_edge_betweenness(graph, weights):
    print('\n+------------------+')
    print('| Edge Betweenness |')
    print('+------------------+')

    start = time.time()
    int_weights = [int(w) for w in weights]
    lpa = graph.community_edge_betweenness(weights=int_weights)
    clus = lpa.as_clustering()
    cluster_index = 0
    for c in clus:
        if cluster_index is 0:
            cluster_index += 1
            continue
        clist = []
        for rep in c:
            if rep is 0:
                continue
            clist.append(convert_vertex(rep))
        print(' Cluster # %d' % cluster_index)
        cluster_index += 1
        ones = [one.split("_")[1] for one in clist if one.startswith('one_')]
        print('\tSide 1:\n\t  ' + str(ones))
        twos = [two.split("_")[1] for two in clist if two.startswith('two_')]
        print('\tSide 2:\n\t  ' + str(twos) + '\n')
    end = time.time()
    print('Modularity of clusters is: ' + str(clus.modularity))
    print('Edge betweenness took ' + str(end-start) + ' seconds.')


def print_header(filename):
    """
    Formatted printing of file name in header of output.
    :param filename: Name of file to visualize.
    """
    raw = filename.split('/')
    filler = ''
    for x in range(len(raw[1])):
        filler += '-'
    border = '+-----------------------------%s-+' % filler
    text = '| Processing data for file -> %s |' % raw[1]
    print(border + '\n' + text + '\n' + border)


if __name__ == '__main__':
    mouse = 'data/final_mouse_weighted.txt'
    print_header(mouse)
    vertices, edges, weights = process_file(mouse)
    plot_data(vertices, edges, weights, 'Mouse', 2)
