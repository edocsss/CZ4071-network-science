from graph.util import data_util, plot_util
from graph.analyzer import clustering_coefficient_analyzer
from graph.analyzer import degree_analyzer
import pandas as pd
import numpy as np
import math


def plot_clustering_coefficient_distribution(network):
    degree_count = degree_analyzer.count_degree(network)
    local_clustering_coeffs = clustering_coefficient_analyzer.calculate_local_clustering_coefficients(network)

    df = pd.DataFrame(data=degree_count.items(), columns=['vid', 'k'])
    k_values = df['k'].unique()

    x = []
    y = []

    for k in k_values:
        vids = df[df.k == k]['vid'].tolist()
        lcc = []

        for vid in vids:
            lcc.append(local_clustering_coeffs[vid])

        x.append(k)
        y.append(np.mean(lcc))

    plot_util.plot_scatter(x, y, title='Log-Log Clustering Coefficient', x_label='k', y_label='C(k)', log_log=True)


def plot_clustering_coefficient_dist_log_binning(network):
    degree_count = degree_analyzer.count_degree(network)
    local_clustering_coeffs = clustering_coefficient_analyzer.calculate_local_clustering_coefficients(network)

    df = pd.DataFrame(data=degree_count.items(), columns=['vid', 'k'])
    k_values = df['k'].unique()

    log_bins = np.logspace(math.log10(min(k_values)), math.log10(max(k_values)), 50)
    x = list((log_bins[1:] + log_bins[:-1]) / 2)
    y = { k: [] for k in range(len(x)) }

    for i in range(len(local_clustering_coeffs)):
        v = network.vertex(i)
        k = v.out_degree()

        for j in range(0, len(log_bins) - 1):
            if log_bins[j] <= k <= log_bins[j + 1]:
                y[j].append(local_clustering_coeffs[i])
                break


    x_prime = []
    y_prime = []

    for l in range(len(y.keys())):
        if len(y[l]) > 0:
            x_prime.append(x[l])
            y_prime.append(sum(y[l]) / len(y[l]))

    plot_util.plot_scatter(x_prime, y_prime, title='Log-Log Clustering Coefficient with Log Binning', x_label='k', y_label='C(k)', log_log=True)


def main():
    network = data_util.get_network()
    print 'Average Clustering Coefficient:', clustering_coefficient_analyzer.calculate_average_clustering_coefficient(network)
    print 'Global Clustering Coefficient:', clustering_coefficient_analyzer.calculate_global_clustering_coefficient(network)
    plot_clustering_coefficient_distribution(network)
    plot_clustering_coefficient_dist_log_binning(network)


if __name__ == '__main__':
    main()