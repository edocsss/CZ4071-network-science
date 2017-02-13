import networkx as nx
from random import choice

G = nx.read_adjlist("static/data/youtube_graph.txt", comments="#")

random_nodes = []
N = 1000

for i in range(N):
    random_node = choice(G.nodes())
    while random_node in random_nodes:
        random_node = choice(G.nodes())
    random_nodes.append(random_node)

# print(random_nodes)

nx.draw(G)