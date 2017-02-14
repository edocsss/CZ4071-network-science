import math
import os
import numpy as np
from graph_tool import clustering, topology
import config as CONFIG
import threading


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


def _shortest_distance_runner(network, thread_id, n_threads=16):
    vertices = list(network.vertices())
    l = len(vertices)

    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'shortest_distance_result_{}.tsv'.format(thread_id))
    f = open(file_path, 'w')
    f.close()

    for i in range(thread_id, l, n_threads):
        v = vertices[i]
        v_id = int(v)
        distance_map = topology.shortest_distance(network, source=v, target=None, directed=False)

        f = open(file_path, 'a')
        f.write('{}'.format(v_id))

        for p in distance_map.get_array():
            f.write('\t{}'.format(p))

        f.write('\n')
        f.close()


def analyze_shortest_distance(network, n_threads=16):
    threads = []
    for i in range(n_threads):
        t = threading.Thread(target=_shortest_distance_runner, args=(network, i, n_threads,))
        print 'Starting thread id:', i
        t.start()
        threads.append(t)

    print 'Threads created!'
    for thread in threads:
        thread.join()

    print 'Done!'