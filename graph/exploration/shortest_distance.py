import cPickle
import os
from multiprocessing import Process

import numpy as np
from graph_tool import topology

from graph.generator import random_network_generator
import config as CONFIG


def _save_object(file_path, obj):
    f = open(file_path, 'wb')
    cPickle.dump(obj, f)
    f.close()


def _load_object(file_path):
    f = open(file_path, 'rb')
    obj = cPickle.load(f)
    f.close()

    return obj


def _shortest_distance_runner_huge_network(network, process_id, n_process=16):
    vertices = list(network.vertices())
    l = len(vertices)

    file_path = os.path.join(
        CONFIG.RESULTS_DIR_PATH,
        'shortest_distance_result_{}.pkl'.format(process_id)
    )

    distance_distribution = {}
    _save_object(file_path, distance_distribution)

    for i in range(process_id, l, n_process):
        distance_distribution = _load_object(file_path)
        v = vertices[i]

        distance_map = topology.shortest_distance(
            network,
            source=v,
            target=None,
            directed=False
        )

        distance_array = distance_map.get_array()[int(v):]
        for j in np.nditer(distance_array):
            distance = int(j)

            if distance not in distance_distribution:
                distance_distribution[distance] = 0

            distance_distribution[distance] += 1

        _save_object(file_path, distance_distribution)


def analyze_shortest_distance(network, n_process=16):
    processes = []
    for i in range(n_process):
        p = Process(
            target=_shortest_distance_runner_huge_network,
            args=(network, i, n_process,)
        )

        print 'Starting process ID:', i
        p.start()
        processes.append(p)

    print 'Processes created!'
    for p in processes:
        p.join()

    print 'Done!'


def main():
    network = random_network_generator.generate_random_network(1000, p=0.35)
    analyze_shortest_distance(network, n_process=4)


if __name__ == '__main__':
    main()
