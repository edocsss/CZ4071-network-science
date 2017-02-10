from util import data_util
import json
import os
import config as CONFIG
import copy


def count_degree():
    network = data_util.get_network()
    counter = {}

    for v in network.vertices():
        vertex_id = int(v)
        counter[vertex_id] = v.out_degree()

    return counter


def analyze_degree_distribution(degree_count=None):
    if degree_count is None:
        degree_count = count_degree()

    degree_distribution = {}
    for k, v in degree_count.items():
        if v not in degree_distribution:
            degree_distribution[v] = 0

        degree_distribution[v] += 1

    for k, v in degree_distribution.items():
        degree_distribution[k] = float(v) / len(degree_count.keys())

    return degree_distribution


def _store_dict_to_json(d, file_name):
    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, file_name)
    f = open(file_path, 'w')
    json.dump(d, f)
    f.close()


if __name__ == '__main__':
    degrees = count_degree()
    _store_dict_to_json(degrees, 'degree_count.json')

    degree_distribution = analyze_degree_distribution()
    _store_dict_to_json(degree_distribution, 'degree_distribution.json')