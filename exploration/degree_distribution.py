from util import data_util
import json
import os
import config as CONFIG
import math
import matplotlib.pyplot as plt


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


def plot_degree_distribution(degree_distribution=None, plot_loglog=False):
    if degree_distribution is None:
        degree_distribution = analyze_degree_distribution()

    x = []
    y = []

    for k, v in degree_distribution.items():
        x.append(k)
        y.append(v)

    if plot_loglog:
        _show_loglog_plot(x, y)
    else:
        _show_usual_plot(x, y)


def _show_loglog_plot(x_log, y_log):
    x_log = [math.log(val) for val in x_log]
    y_log = [math.log(val) for val in y_log]
    _show_usual_plot(x_log, y_log)


def _show_usual_plot(x, y):
    plt.scatter(x, y, s=20*0.01)
    plt.show()


def _store_dict_to_json(d, file_name):
    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, file_name)
    f = open(file_path, 'w')
    json.dump(d, f)
    f.close()


def calculate_moment(degree_count, n=1):
    return sum([math.pow(c, n) for c in degree_count.values()]) / len(degree_count.values())


if __name__ == '__main__':
    degrees = count_degree()
    _store_dict_to_json(degrees, 'degree_count.json')

    degree_distribution = analyze_degree_distribution()
    _store_dict_to_json(degree_distribution, 'degree_distribution.json')

    first_moment = calculate_moment(degrees, n=1)
    second_moment = calculate_moment(degrees, n=2)

    print('First Moment:', first_moment)
    print('Second Moment:', second_moment)

    plot_degree_distribution(degree_distribution, plot_loglog=False)