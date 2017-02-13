import json
import math
import os

import matplotlib.pyplot as plt
from graph.util import data_util

import config as CONFIG
from graph.util import network_util


def plot_degree_distribution(degree_distribution, plot_loglog=False):
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


if __name__ == '__main__':
    network = data_util.get_network()
    degree_count = network_util.count_degree(network)
    _store_dict_to_json(degree_count, 'degree_count.json')

    degree_distribution = network_util.analyze_degree_distribution(degree_count)
    _store_dict_to_json(degree_distribution, 'degree_distribution.json')

    first_moment = network_util.calculate_moment(degree_count, n=1)
    second_moment = network_util.calculate_moment(degree_count, n=2)
    print('First Moment:', first_moment)
    print('Second Moment:', second_moment)

    plot_degree_distribution(degree_distribution, plot_loglog=False)