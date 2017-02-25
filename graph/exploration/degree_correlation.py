import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from graph.analyzer import degree_analyzer
from graph.util import data_util, plot_util


def get_all_possible_degree_values(network):
    return { v.out_degree() for v in network.vertices() }


def get_edge_probs_distribution(network):
    edge_distribution = {}
    for e in network.edges():
        source_degree = e.source().out_degree()
        target_degree = e.target().out_degree()
        edge_pair = (source_degree, target_degree) if source_degree < target_degree else (target_degree, source_degree)

        if edge_pair not in edge_distribution:
            edge_distribution[edge_pair] = 0

        edge_distribution[edge_pair] += 1

    no_of_edges = network.num_edges()
    for k, v in edge_distribution.items():
        edge_distribution[k] = float(v) / float(no_of_edges)

    return edge_distribution


def calculate_qk(k, degree_probs_distribution, avg_degree):
    return float(k * degree_probs_distribution[k]) / float(avg_degree)


def calculate_p_k_given_k_prime(k, k_prime, degree_probs_distribution, avg_degree, edge_probs_distribution):
    qk = calculate_qk(k, degree_probs_distribution, avg_degree)
    edge_pair = (k, k_prime) if k < k_prime else (k_prime, k)
    ek_kprime = edge_probs_distribution[edge_pair] if edge_pair in edge_probs_distribution else 0
    return float(ek_kprime) / float(qk)


def analyze_degree_correlation(network):
    n = network.num_vertices()
    degree_count = degree_analyzer.count_degree(network)
    degree_distribution = degree_analyzer.calculate_degree_distribution(degree_count)
    degree_probs_distribution = degree_analyzer.calculate_degree_prob_distribution(n, degree_distribution)
    avg_degree = degree_analyzer.calculate_degree_moment(degree_count, n=1)

    possible_k = get_all_possible_degree_values(network)
    edge_probs_distribution = get_edge_probs_distribution(network)

    knn = {}
    print 'Start..'
    for k in possible_k:
        total = 0
        for k_prime in possible_k:
            total += k_prime * calculate_p_k_given_k_prime(
                k,
                k_prime,
                degree_probs_distribution,
                avg_degree,
                edge_probs_distribution
            )

        knn[k] = total

    return knn


def plot_degree_correlations(degree_correlations, log_log=False):
    x = []
    y = []

    for k, v in degree_correlations.items():
        if log_log:
            x.append(math.log10(k))
            y.append(math.log10(v))
        else:
            x.append(k)
            y.append(v)

    plt.clf()
    plt.scatter(x=x, y=y, s=2, c='r')
    plt.title('Log-Log Degree Correlations')
    plt.xlabel('k')
    plt.ylabel('knn(k)')
    plt.show()


def plot_log_binned_degree_correlations(network, degree_correlations):
    degree_count = degree_analyzer.count_degree(network)
    df = pd.DataFrame(data=degree_count.items(), columns=['vid', 'k'])
    k_values = df['k'].unique()

    log_bins = np.logspace(math.log10(min(k_values)), math.log10(max(k_values)), 50)
    x = list((log_bins[1:] + log_bins[:-1]) / 2)
    y = {k: [] for k in range(len(x))}

    deg = degree_correlations.items()
    for i in range(len(deg)):
        for j in range(0, len(log_bins) - 1):
            if log_bins[j] <= deg[i][0] <= log_bins[j + 1]:
                y[j].append(deg[i][1])
                break

    x_prime = []
    y_prime = []

    for l in range(len(y.keys())):
        if len(y[l]) > 0:
            x_prime.append(x[l])
            y_prime.append(sum(y[l]) / len(y[l]))

    plot_util.plot_scatter(x_prime, y_prime, title='Log-Log Degree Correlation with Log Binning', x_label='k',
                           y_label='knn(k)', log_log=True)


if __name__ == '__main__':
    network = data_util.get_network()
    degree_correlations = analyze_degree_correlation(network)
    plot_degree_correlations(degree_correlations, log_log=True)
    plot_log_binned_degree_correlations(network, degree_correlations)