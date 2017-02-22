from graph.util import data_util, plot_util
from graph.analyzer import degree_analyzer
import time
import os
import math
import config as CONFIG
import matplotlib.pyplot as plt
import numpy as np


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
    plt.title('Degree Correlations')
    plt.xlabel('k')
    plt.ylabel('knn(k)')
    plt.show()


def plot_log_binned_degree_correlations(degree_correlations):
    n, bins = plot_util.log_binning(degree_correlations, n_bins=100)
    bin_centers = list((bins[1:] + bins[:-1]) / 2)
    n = list(n)

    plot_util.plot_scatter(
        bin_centers,
        n,
        title='Log-Log Degree Correlations with Log Binning',
        x_label='k',
        y_label='knn(k)',
        log_log=True
    )


if __name__ == '__main__':
    network = data_util.get_network()
    degree_correlations = analyze_degree_correlation(network)
    # plot_degree_correlations(degree_correlations, log_log=True)
    plot_log_binned_degree_correlations(degree_correlations)