import networkx as nx
import matplotlib.pyplot as plt


def parseData(graph_name):
    f = open("../" + graph_name)
    # skip the first bit of file to get to first data line
    for x in range(0, 26):
        f.readline()
    content = f.read().splitlines()
    content = [x.split(',') for x in content]
    indexes = [1, 3]
    graph_data = []
    for line in content:
        if line[6] == "yes":
            print line
            graph_data.append([line[data] for data in indexes])
    return graph_data


def writeData(graph_data):
    f = open('parsed.csv', 'w')
    for line in graph_data:
        f.write(line[0] + "," + line[1] + "\n")


G = nx.Graph()
graph_data = parseData("unprocessed_data.csv")
graph_data.pop(8315)
writeData(graph_data)
G.add_edges_from(graph_data)
G.name = 'Mouse Connectome'
print("\n" + nx.info(G) + "\n")

plt.figure(figsize=(12, 12), dpi=1200)
pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=60, node_color='lightblue',
        linewidths=0.25, font_size=8, font_weight='bold', with_labels=True)
plt.savefig('labels.pdf')
