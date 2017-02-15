from multiprocessing import Process, Queue
from graph_tool import topology
import numpy as np


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

    total = sum([k * v for k, v in distance_distribution.items()])
    max_no_of_edges = no_of_nodes * (no_of_nodes - 1) / 2
    return float(total) / float(max_no_of_edges)


def find_network_diameter(distance_distribution):
    if distance_distribution is None:
        return None

    return max(distance_distribution.keys())


def calculate_distance_prob_distribution(distance_distribution):
    if distance_distribution is None:
        return None

    total = sum(distance_distribution.values())
    for k, v in distance_distribution.items():
        distance_distribution[k] /= float(total)

    return distance_distribution


if __name__ == '__main__':
    from graph.generator import random_network_generator

    network = random_network_generator.generate_random_network(1000, p=0.746)
    distance_distribution = get_distance_distribution(network, n_process=2)
    print distance_distribution

    print calculate_average_distance(network.num_vertices(), distance_distribution)
    print find_network_diameter(distance_distribution)
    print calculate_distance_prob_distribution(distance_distribution)