import math


def count_degree(network):
    counter = {}
    for v in network.vertices():
        vertex_id = int(v)
        counter[vertex_id] = v.out_degree()

    return counter


def calculate_degree_distribution(degree_count):
    degree_distribution = {}
    for k, v in degree_count.items():
        if v not in degree_distribution:
            degree_distribution[v] = 0

        degree_distribution[v] += 1

    return degree_distribution


def calculate_degree_prob_distribution(no_of_nodes, degree_distribution):
    for k, v in degree_distribution.items():
        degree_distribution[k] = float(v) / no_of_nodes

    return degree_distribution


def calculate_degree_moment(degree_count, n=1):
    return sum([
        math.pow(c, n) for c in degree_count.values()
    ]) / len(degree_count.values())


def find_largest_degree(degree_distribution):
    return max(degree_distribution.keys())


def find_smallest_degree(degree_distribution):
    return min(degree_distribution.keys())