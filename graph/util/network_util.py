import math
import os
import numpy as np
from graph_tool import clustering, topology
import config as CONFIG
from multiprocessing import Process
from graph.util import plot_util
from scipy.stats import linregress
import matplotlib.pyplot as plt
import logging
import cPickle
import gzip
logger = logging.getLogger(__name__)


def save(obj, file_path):
    f = gzip.GzipFile(file_path, 'wb')
    cPickle.dump(obj, f, cPickle.HIGHEST_PROTOCOL)
    f.close()


def load(file_path):
    f = gzip.GzipFile(file_path, 'rb')
    obj = cPickle.load(f)
    f.close()

    return obj


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


def calculate_degree_exponent(degree_count, plot=False):
    n, bins = plot_util.log_binning(degree_count, n_bins=50)
    bin_centers = list((bins[1:] + bins[:-1]) / 2)
    n = list(n)

    x_log, y_log = plot_util.get_log_log_points(bin_centers, n)
    slope, intercept, _, _, _ = linregress(x_log, y_log)

    xl = [math.log10(i) for i in range(1, 10000)]
    yl = [slope * math.log10(i) + intercept for i in range(1, 10000)]

    if plot:
        plt.plot(xl, yl, 'r')
        plot_util.plot_scatter(bin_centers, n, title='Log-Log Degree Distribution', x_label='k', y_label='P(k)',
                               log_log=True)

    return slope


def _shortest_distance_runner_small_network(network, thread_id, n_threads=8):
    vertices = list(network.vertices())
    l = len(vertices)

    for i in range(thread_id, l, n_threads):
        v = vertices[i]
        v_id = int(v)

        distance_map = topology.shortest_distance(network, source=v, target=None, directed=False)
        distance_array = distance_map.get_array()


def instant_shortest_distance(network, n_process=4):
    n_nodes = network.num_vertices()
    if n_nodes > 100000:
        return None

    processes = []
    for i in range(n_process):
        p = Process(target=_shortest_distance_runner_small_network, args=(network, i, n_process,))
        print 'Starting process ID:', i
        p.start()
        processes.append(p)

    print 'Processes created!'
    for p in processes:
        p.join()

    print 'Done!'
