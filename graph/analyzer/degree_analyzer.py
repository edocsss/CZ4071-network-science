import math


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


def calculate_degree_moment(degree_count, n=1):
    return sum([
        math.pow(c, n) for c in degree_count.values()
    ]) / len(degree_count.values())