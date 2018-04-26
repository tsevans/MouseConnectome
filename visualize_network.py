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
    print('\t# of nodes --> ' + str(len(proc_vertices)))
    print('\t# of edges --> ' + str(len(proc_edges)))
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


def plot_data(vertices, edges, fname):
    graph = ig.Graph(edges, directed=False)
    colors = []
    for v in vertices:
        c = ColorHash(v)
        # if v.startswith('A'):
        #     colstr = 'rgb(255,' + str(int(c.rgb[1])) + ',0)'
        # elif v.startswith('V'):
        #     colstr = 'rgb(0,' + str(int(c.rgb[1])) + ',255)'
        # else:
        #     colstr = 'rgb(0,255,' + str(int(c.rgb[1])) + ')'
        #colstr = 'rgb(' + str(int(c.rgb[0])) + ',' + str(int(c.rgb[1])) + ',' + str(int(c.rgb[2])) + ')'
        colstr = colstr = 'rgb(0,255,' + str(int(c.rgb[2])) + ')'
        colors.append(colstr)

    # Spatial layout of graph components
    layt = graph.layout('kk', dim=3)

    x_vertex = [layt[k][0] for k in range(len(vertices))]  # x-coordinates of nodes
    y_vertex = [layt[k][1] for k in range(len(vertices))]  # y-coordinates of nodes
    z_vertex = [layt[k][2] for k in range(len(vertices))]  # z-coordinates of nodes
    x_edge = []
    y_edge = []
    z_edge = []
    for e in edges:
        x_edge += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
        y_edge += [layt[e[0]][1], layt[e[1]][1], None]  # y-coordinates of edge ends
        z_edge += [layt[e[0]][2], layt[e[1]][2], None]  # z-coordinates of edge ends

    edge_trace = Scatter3d(
        x=x_edge,
        y=y_edge,
        z=z_edge,
        mode='lines',
        line=Line(color='rgb(0,0,0)', width=1),
        hoverinfo='none'
    )

    vertex_trace = Scatter3d(
        x=x_vertex,
        y=y_vertex,
        z=z_vertex,
        mode='markers',
        name='cortical areas',
        marker=Marker(
            symbol='dot',
            size=9,
            color=colors,
            line=Line(color='rgb(50,50,50)', width=0.5)
        ),
        text=vertices,
        hoverinfo='text'
    )

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    layout = Layout(
        title="3D visualization of macaque cortical area network",
        showlegend=False,
        scene=Scene(
            xaxis=XAxis(axis),
            yaxis=YAxis(axis),
            zaxis=ZAxis(axis),
        ),
        margin=Margin(
            t=100
        ),
        hovermode='closest')

    data = Data([edge_trace, vertex_trace])
    fig = Figure(data=data, layout=layout)
    py.plot(fig, filename='./' + fname + '.html')


def generate_macaque_one():
    print('+======================+\n| Macaque Connectome # 1 |\n+======================+')
    vertices, edges = process_file('macaque_one.txt')
    plot_data(vertices, edges, 'Macaque_One')


def generate_macaque_two():
    print('+======================+\n| Macaque Connectome # 2 |\n+======================+')
    vertices, edges = process_file('macaque_two.txt')
    plot_data(vertices, edges, 'Macaque_Two')


def generate_macaque_three():
    print('+======================+\n| Macaque Connectome # 3 |\n+======================+')
    vertices, edges = process_file('macaque_three.txt')
    plot_data(vertices, edges, 'Macaque_Three')


def generate_cat():
    print('+==============+\n| Cat Connectome |\n+==============+')
    vertices, edges = process_file('cat.txt')
    plot_data(vertices, edges, 'Cat')


def generate_mouse():
    print('+==================+\n| Mouse Connectome |\n+==================+')

    # g = read_graph_from_file('mouse.txt')
    # g = lpa(g, 6)
    # print_graph_info(g)
    #
    # node_color = []
    # for v in g:
    #     random.seed(g.node[v]['current_label'].keys()[0])
    #     node_color.append(float(random.random()))
    # labels = dict([(node, node) for node in g.nodes()])
    # nx.draw_networkx(g, node_color=node_color, with_labels=False, node_size=25)
    # plt.show()

    vertices, edges = process_file('mouse.txt')
    plot_data(vertices, edges, 'Mouse')


if __name__ == '__main__':
    #generate_mouse()
    generate_cat()
    # generate_macaque_one()
    # generate_macaque_two()
    # generate_macaque_three()
