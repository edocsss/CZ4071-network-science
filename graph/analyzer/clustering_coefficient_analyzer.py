from graph_tool import clustering
import numpy as np


def calculate_global_clustering_coefficient(network):
    global_clustering_coefficient = clustering.global_clustering(network)
    return global_clustering_coefficient[0]


def calculate_average_clustering_coefficient(network):
    lc = clustering.local_clustering(network, undirected=True)
    coeffs = lc.get_array()
    return float(np.sum(coeffs) / len(coeffs))
