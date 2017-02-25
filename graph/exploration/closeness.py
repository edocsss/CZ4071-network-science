import cPickle
import math
import os

import numpy as np
import pandas as pd
from graph_tool import centrality

import config as CONFIG
from graph.analyzer import degree_analyzer
from graph.util import data_util, plot_util


def analyze_closeness(_network):
    closeness = centrality.closeness(_network)

    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'closeness.pkl')
    f = open(file_path, 'wb')
    cPickle.dump(closeness, f, cPickle.HIGHEST_PROTOCOL)
    f.close()


def read_closeness_result():
    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'closeness.pkl')
    f = open(file_path, 'rb')
    closeness = cPickle.load(f)
    f.close()

    return closeness.get_array()


def calculate_closeness_k_bk(closeness, network):
    result = {}

    for i in range(len(closeness)):
        v = network.vertex(i)
        k = v.out_degree()

        if k not in result:
            result[k] = []

        result[k].append(closeness[i])

    for k, v in result.items():
        result[k] = sum(v) / len(v)

    return result


def plot_closeness_k_bk(closeness_distribution, log_log=True):
    x = []
    y = []

    for k, v in closeness_distribution.items():
        x.append(k)
        y.append(v)

    plot_util.plot_scatter(x, y, title='Log-Log Closeness Distribution', x_label='k', y_label='Cl(k)', log_log=log_log)


def plot_closeness_k_bk_log_binning(network, closeness):
    degree_count = degree_analyzer.count_degree(network)
    df = pd.DataFrame(data=degree_count.items(), columns=['vid', 'k'])
    k_values = df['k'].unique()

    log_bins = np.logspace(math.log10(min(k_values)), math.log10(max(k_values)), 50)
    x = list((log_bins[1:] + log_bins[:-1]) / 2)
    y = {k: [] for k in range(len(x))}

    for i in range(len(closeness)):
        v = network.vertex(i)
        k = v.out_degree()

        for j in range(0, len(log_bins) - 1):
            if log_bins[j] <= k <= log_bins[j + 1]:
                y[j].append(closeness[i])
                break

    x_prime = []
    y_prime = []

    for l in range(len(y.keys())):
        if len(y[l]) > 0:
            x_prime.append(x[l])
            y_prime.append(sum(y[l]) / len(y[l]))

    plot_util.plot_scatter(x_prime, y_prime, title='Log-Log Closeness Distribution with Log Binning', x_label='k',
                           y_label='Cl(k)', log_log=True)


if __name__ == '__main__':
    network = data_util.get_network()
    closeness = read_closeness_result()
    c_distribution = calculate_closeness_k_bk(closeness, network)
    plot_closeness_k_bk(c_distribution, log_log=True)
    plot_closeness_k_bk_log_binning(network, closeness)