import igraph as ig
import plotly.offline as py
from plotly.graph_objs import *
from colorhash import ColorHash
from copra_lpa import *

vertex_index = {}


def convert_vertex(v):
    if type(v) is int:
        reverse_index = dict((v, k) for k, v in vertex_index.iteritems())
        return reverse_index[v]
    return vertex_index[v]


def process_file(filename):
    edge_file = open(filename)
    line_list = edge_file.readlines()
    proc_vertices = parse_line_vertices(line_list)
    proc_edges = parse_line_edges(line_list)
    edge_file.close()
    print(str(len(proc_vertices)) + ' vertices')
    print(str(len(proc_edges)) + ' edges')
    return proc_vertices, proc_edges


def parse_line_edges(line_list):
    edge_list = []
    for ln in line_list:
        parts = ln.split()
        src = convert_vertex(parts[0])
        dst = convert_vertex(parts[1])
        edge_list.append((src, dst))
    return edge_list


def parse_line_vertices(line_list):
    vertex_map = {}
    edge_list = []
    val_count = 1
    for ln in line_list:
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


def plot_data(vertices, edges, f_name):
    """
    Plot network data in three-dimensional space.
    :param vertices: List of vertices in the network.
    :param edges: List of connections in the network.
    :param f_name: Name of HTML file to generate.
    """
    graph = ig.Graph(edges, directed=False)
    colors = []
    for v in vertices:
        c = ColorHash(v)
        colors.append('rgb(%s,%s,%s)' % tuple(c.rgb))

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

        layout = Layout(title="3D visualization of macaque cortical area network",
                        showlegend=False,
                        scene=Scene(xaxis=XAxis(axis), yaxis=YAxis(axis), zaxis=ZAxis(axis), ),
                        margin=Margin(t=100),
                        hovermode='closest')
        return layout

    data = Data([trace_edges(edges, spatial),
                 trace_vertices(vertices, spatial)])
    fig = Figure(data=data, layout=build_layout())
    py.plot(fig, filename='output/' + f_name + '.html')


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
    test_cat = 'data/cat.txt'
    print_header(test_cat)
    vertices, edges = process_file(test_cat)
    plot_data(vertices, edges, 'Cat')
