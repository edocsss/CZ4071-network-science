import os
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
from graph_tool import topology
import numpy as np
import config as CONFIG


def _shortest_distance_runner_small_network(result_queue, network, thread_id, n_threads=8):
    vertices = list(network.vertices())
    l = len(vertices)
    distance_distribution = {}

    for i in range(thread_id, l, n_threads):
        v = vertices[i]
        v_id = int(v)

        distance_map = topology.shortest_distance(
            network,
            source=v,
            target=None,
            directed=False
        )

        distance_array = distance_map.get_array()[v_id:]
        for j in np.nditer(distance_array):
            distance = int(j)

            if distance not in distance_distribution:
                distance_distribution[distance] = 0

            distance_distribution[distance] += 1

    result_queue.put(distance_distribution)


def _convert_multiprocessing_queue_to_list(queue):
    result = []
    while not queue.empty():
        result.append(queue.get())

    return result


def combine_multiple_distance_distributions(distance_distribution_list):
    result = {}

    for distance_distribution in distance_distribution_list:
        for k, v in distance_distribution.items():
            if k not in result:
                result[k] = 0

            result[k] += v

    return result



def get_distance_distribution(network, n_process=4):
    n_nodes = network.num_vertices()
    if n_nodes > 10000:
        return None

    processes = []
    result_queue = Queue(n_process)
    for i in range(n_process):
        p = Process(
            target=_shortest_distance_runner_small_network,
            args=(result_queue, network, i, n_process,)
        )

        print 'Starting process ID:', i
        p.start()
        processes.append(p)

    print 'Processes created!'
    for p in processes:
        p.join()

    print 'Done!'

    result_list = _convert_multiprocessing_queue_to_list(result_queue)
    return combine_multiple_distance_distributions(result_list)



def calculate_average_distance(no_of_nodes, distance_distribution):
    if distance_distribution is None:
        return None

    total = sum([k * v for k, v in distance_distribution.items() if int(k) <= sum(distance_distribution.values())])
    max_no_of_edges = no_of_nodes * (no_of_nodes - 1) / 2
    return float(total) / float(max_no_of_edges)


def find_network_diameter(distance_distribution):
    if distance_distribution is None:
        return None

    print distance_distribution
    return max([k for k in distance_distribution.keys() if int(k) <= sum(distance_distribution.values())])


def calculate_distance_prob_distribution(distance_distribution):
    result = {}
    if distance_distribution is None:
        return None

    total = sum(distance_distribution.values())
    for k, v in distance_distribution.items():
        if k > total or k == 0:
            continue

        result[k] = float(distance_distribution[k]) / float(total)

    return result


def plot_and_store_distance_prob_distribution(network_name, distance_prob_distribution):
    file_name = network_name + '_distance_distribution.png'
    file_path = os.path.join(CONFIG.DB_PLOT_DIR_PATH, file_name)
    print distance_prob_distribution

    x = []
    y = []

    for k, v in distance_prob_distribution.items():
        x.append(k)
        y.append(v)

    plt.clf()
    plt.scatter(x, y, c='r')
    plt.title('Shortest Distance Distribution')
    plt.xlabel('d')
    plt.ylabel('P(d)')
    plt.savefig(file_path)
    plt.close()

    return file_name


if __name__ == '__main__':
    from graph.generator import random_network_generator

    network = random_network_generator.generate_random_network(1000, p=0.746)
    distance_distribution = get_distance_distribution(network, n_process=2)
    print distance_distribution

    print calculate_average_distance(network.num_vertices(), distance_distribution)
    print find_network_diameter(distance_distribution)
    print calculate_distance_prob_distribution(distance_distribution)