from graph.util import data_util
import config as CONFIG
import os
from graph_tool import topology
import numpy as np
from multiprocessing import Process
import gzip
import cPickle


def _shortest_distance_runner_huge_network(network, process_id, n_process=16):
    vertices = list(network.vertices())
    l = len(vertices)

    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'shortest_distance_result_{}.pkl'.format(process_id))
    distance_distribution = {}

    for i in range(process_id, l, n_process):
        v = vertices[i]
        distance_map = topology.shortest_distance(network, source=v, target=None, directed=False)
        distance_array = distance_map.get_array()

        for j in np.nditer(distance_array):
            distance = int(j)
            if distance not in distance_distribution:
                distance_distribution[distance] = 0

            distance_distribution[distance] += 1

    f = gzip.GzipFile(file_path, 'wb')
    cPickle.dump(distance_distribution, f, cPickle.HIGHEST_PROTOCOL)
    f.close()


def analyze_shortest_distance(network, n_process=16):
    processes = []
    for i in range(n_process):
        p = Process(target=_shortest_distance_runner_huge_network, args=(network, i, n_process,))
        print 'Starting process ID:', i
        p.start()
        processes.append(p)

    print 'Processes created!'
    for p in processes:
        p.join()

    print 'Done!'


if __name__ == '__main__':
    network = data_util.get_network()
    analyze_shortest_distance(network, n_process=1)
