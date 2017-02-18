import json
import math
import os

import matplotlib.pyplot as plt

import config as CONFIG
from graph.util import data_util, plot_util
from graph.analyzer import degree_analyzer


def plot_degree_distribution(deg_dist, plot_loglog=False):
    x = []
    y = []

    for k, v in deg_dist.items():
        x.append(k)
        y.append(v)

    if plot_loglog:
        _show_loglog_plot(x, y, 'Log-Log Degree Distribution', 'k', 'P(k)')
    else:
        _show_usual_plot(x, y, 'Degree Distribution', 'k', 'P(k)')


def plot_log_binned_degree_distribution(deg_count):
    n, bins = plot_util.log_binning(deg_count, n_bins=50, plot=True)
    bin_centers = list((bins[1:] + bins[:-1]) / 2)
    n = list(n)
    plot_util.plot_scatter(
        bin_centers,
        n,
        title='Log-Log Degree Distribution with Log Binning',
        x_label='k',
        y_label='P(k)',
        log_log=True
    )


def _show_loglog_plot(x, y, title, x_label, y_label):
    x_log = [math.log(val) for val in x]
    y_log = [math.log(val) for val in y]
    _show_usual_plot(x_log, y_log, title, x_label, y_label)


def _show_usual_plot(x, y, title, x_label, y_label):
    plot_util.plot_scatter(
        x=x,
        y=y,
        s=20*0.01,
        c='r',
        title=title,
        x_label=x_label,
        y_label=y_label
    )


def _store_dict_to_json(d, file_name):
    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, file_name)
    f = open(file_path, 'w')
    json.dump(d, f)
    f.close()


def main():
    network = data_util.get_network()
    degree_count = degree_analyzer.count_degree(network)
    _store_dict_to_json(degree_count, 'degree_count.json')

    degree_distribution = degree_analyzer.calculate_degree_distribution(degree_count)
    degree_prob_distribution = degree_analyzer.calculate_degree_prob_distribution(network.num_vertices(), degree_distribution)
    _store_dict_to_json(degree_prob_distribution, 'degree_prob_distribution.json')

    first_moment = degree_analyzer.calculate_degree_moment(degree_count, n=1)
    second_moment = degree_analyzer.calculate_degree_moment(degree_count, n=2)
    print('First Moment:', first_moment)
    print('Second Moment:', second_moment)

    kmax = degree_analyzer.find_largest_degree(degree_distribution)
    kmin = degree_analyzer.find_smallest_degree(degree_distribution)
    print 'Largest Degree:', kmax
    print 'Smallest Degree:', kmin

    plot_degree_distribution(degree_prob_distribution, plot_loglog=True)
    plot_log_binned_degree_distribution(degree_count)
    print degree_analyzer.plot_and_store_degree_prob_distribution('youtube', degree_count)


if __name__ == '__main__':
    main()
