import math
import numpy as np
from graph_tool import clustering, topology
import cPickle
import os
import config as CONFIG


def count_degree(network):
    counter = {}
    for v in network.vertices():
        vertex_id = int(v)
        counter[vertex_id] = v.out_degree()

    return counter


def analyze_degree_distribution(degree_count):
    degree_distribution = {}
    for k, v in degree_count.items():
        if v not in degree_distribution:
            degree_distribution[v] = 0

        degree_distribution[v] += 1

    for k, v in degree_distribution.items():
        degree_distribution[k] = float(v) / len(degree_count.keys())

    return degree_distribution


def calculate_moment(degree_count, n=1):
    return sum([math.pow(c, n) for c in degree_count.values()]) / len(degree_count.values())


def calculate_global_clustering_coefficient(network):
    global_clustering_coefficient = clustering.global_clustering(network)
    return global_clustering_coefficient[0]


def calculate_average_clustering_coefficient(network):
    lc = clustering.local_clustering(network, undirected=True)
    coeffs = lc.get_array()
    return np.sum(coeffs) / len(coeffs)


def store_shortest_distance(network):
    props = topology.shortest_distance(network, source=None, target=None, directed=False)
    file_path = os.path.join(CONFIG.DATA_DIR_PATH, 'shortest_distance_props.pkl')

    f = open(file_path, 'wb')
    cPickle.dump(props, f)
    f.close()