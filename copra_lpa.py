import random
import networkx as nx
import matplotlib.pyplot as plt


def read_graph_from_file(path):
    # read edge-list from file
    graph = nx.Graph()
    fl = open(path)
    weighted_edges = []
    for ln in fl.readlines():
        weighted_edges.append(tuple(ln.split()))
    graph.add_weighted_edges_from(weighted_edges)

    #graph = nx.read_edgelist(path, data=(('weight', float),))

    # initial graph's node's attribute 'label' with its id
    for node, data in graph.nodes(True):
        data['prev_label'] = {node: 1.0}
        data['current_label'] = dict()

    return graph


def read_game_info_from_file(path):
    game = {}

    with file(path, 'r') as f:
        for line in f:
            line = line.strip()
            data = line.split('\t')
            game[data[0]] = data[1]

    return game


def read_mouse_info(path):
    game = {}

    with file(path, 'r') as f:
        for line in f:
            line = line.strip()
            data = line.split('\t')
            game[data[0]] = data[1]

    return game


# COPRA - label-propagation algorithm
# (can find overlapping communities)
#
# note:
#     use synchronous updating for better results
#
# parameter:
#     v : number of labels of a vertex can contain
def lpa(graph, v):
    """

    :param graph:
    :param v:
    :return:
    """

    def propagate(vertex):
        """
        Propagation phase of algorithm using synchronous updating scheme.
        :param vertex:
        """
        'calculate belonging coefficient'
        # we assume that current label dict is empty
        # store vertex -> belonging coefficient
        current_label = graph.node[vertex]['current_label']

        degree = graph.degree(vertex)
        for neighbor in graph.neighbors(vertex):
            prev_label = graph.node[neighbor]['prev_label']

            for label in prev_label:
                current_label[label] = current_label.get(label, 0.0) \
                                       + prev_label[label] / degree

        normalize(current_label)

        # delete pair that is less then threshold
        threshold = 1.0 / v
        deleted_labels, coefficient_max = set(), 0.0
        for label, coefficient in current_label.items():
            if coefficient < threshold:
                del current_label[label]
                if coefficient > coefficient_max:
                    deleted_labels.clear()
                    deleted_labels.add(label)
                    coefficient_max = coefficient
                elif coefficient == coefficient_max:
                    deleted_labels.add(label)

        if len(current_label) == 0:
            current_label[random.sample(deleted_labels, 1)[0]] = 1.0
        else:
            normalize(current_label)

    def normalize(labels):
        """
        Normalize coefficients so that they sum to 1
        """
        sum_val = sum(labels.values())
        if sum_val == 1:
            return
        for label in labels:
            labels[label] = labels[label] / sum_val

    def reset_current_label():
        for node in graph.nodes():
            graph.node[node]['prev_label'] = graph.node[node]['current_label']
            graph.node[node]['current_label'] = dict()

    def label_set(label_type):
        labels = set()
        for node in graph.nodes():
            labels.update(graph.node[node][label_type].keys())
        return labels

    def label_count(label_type):
        labels = dict()
        for node in graph.nodes():
            for label in graph.node[node][label_type]:
                labels[label] = labels.get(label, 0) + 1
        return labels

    def mc(label_dict_1, label_dict_2):
        label_dict = dict()
        for label in label_dict_1:
            label_dict[label] = min(label_dict_1[label], label_dict_2[label])
        return label_dict

    min_labels = dict()
    old_min_labels = dict()
    loop_count = 0
    while True:
        loop_count += 1
        print 'loop', loop_count

        for node in graph.nodes():
            propagate(node)

        prev_label_set = label_set('prev_label')
        current_label_set = label_set('current_label')

        if prev_label_set == current_label_set:
            min_labels = mc(min_labels, label_count('current_label'))
        else:
            min_labels = label_count('current_label')

        if min_labels != old_min_labels:
            old_min_labels = min_labels
            reset_current_label()
            continue

        return graph


def print_graph_info(graph):
    game_info = read_mouse_info('data/mouse_regions.txt')
    info = {}

    for node in graph.nodes():
        parts = str(node).split('_')
        current_label = graph.node[node]['current_label']

        for label in current_label:
            info.setdefault(label, []).append(game_info.get(parts[1], node))

    print 'node num:', len(graph.nodes())
    print 'class num:', len(info.keys())
    print 'class:', info.keys()
    print 'info:'
    for clazz in info:
        print("------------------------------------------")
        print '%s(%d):\n' % (clazz, len(info[clazz])),
        for label in info[clazz]:
            print('\t' + str(label).strip('"'))
        print '\n',


if __name__ == '__main__':
    #g = read_graph_from_file('f.data')
    g = read_graph_from_file('data/final_mouse_weighted.txt')
    g = lpa(g, 30)
    print_graph_info(g)

    #node_color = [float(g.node[v]['current_label'].keys()[0]) for v in g]
    node_color = []
    for v in g:
        random.seed(g.node[v]['current_label'].keys()[0])
        node_color.append(float(random.random()))
    labels = dict([(node, node) for node in g.nodes()])
    nx.draw_networkx(g, node_color=node_color)
    plt.show()
