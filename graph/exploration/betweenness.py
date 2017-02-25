from graph_tool import centrality
import os
import cPickle
import math

import numpy as np
import pandas as pd

from graph.util import data_util, plot_util
from graph.analyzer import degree_analyzer
import config as CONFIG


def analyze_betweenness(_network):
    vb, eb = centrality.betweenness(_network)

    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'vertex_betweenness.pkl')
    f = open(file_path, 'wb')
    cPickle.dump(vb.get_array(), f, cPickle.HIGHEST_PROTOCOL)
    f.close()


def read_betweenness_result():
    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'vertex_betweenness.pkl')
    f = open(file_path, 'rb')
    vb = cPickle.load(f)
    f.close()

    return vb


def calculate_betweenness_k_bk(betweenness, network):
    result = {}

    for i in range(len(betweenness)):
        v = network.vertex(i)
        k = v.out_degree()

        if k not in result:
            result[k] = []

        result[k].append(betweenness[i])

    for k, v in result.items():
        result[k] = sum(v) / len(v)

    return result


def plot_betweenness_k_bk(betweenness_distribution, log_log=True):
    x = []
    y = []

    for k, v in betweenness_distribution.items():
        x.append(k)
        y.append(v)

    plot_util.plot_scatter(x, y, title='Log-Log Betweenness Distribution', x_label='k', y_label='B(k)', log_log=log_log)


def plot_betweenness_k_bk_log_binning(network, betweenness):
    degree_count = degree_analyzer.count_degree(network)
    df = pd.DataFrame(data=degree_count.items(), columns=['vid', 'k'])
    k_values = df['k'].unique()

    log_bins = np.logspace(math.log10(min(k_values)), math.log10(max(k_values)), 50)
    x = list((log_bins[1:] + log_bins[:-1]) / 2)
    y = {k: [] for k in range(len(x))}

    for i in range(len(betweenness)):
        v = network.vertex(i)
        k = v.out_degree()

        for j in range(0, len(log_bins) - 1):
            if log_bins[j] <= k <= log_bins[j + 1]:
                y[j].append(betweenness[i])
                break

    x_prime = []
    y_prime = []

    for l in range(len(y.keys())):
        if len(y[l]) > 0:
            x_prime.append(x[l])
            y_prime.append(sum(y[l]) / len(y[l]))

    plot_util.plot_scatter(x_prime, y_prime, title='Log-Log Betweenness Distribution with Log Binning', x_label='k',
                           y_label='B(k)', log_log=True)


if __name__ == '__main__':
    network = data_util.get_network()
    betweenness = read_betweenness_result()
    b_distribution = calculate_betweenness_k_bk(betweenness, network)
    plot_betweenness_k_bk(b_distribution, log_log=True)
    plot_betweenness_k_bk_log_binning(network, betweenness)