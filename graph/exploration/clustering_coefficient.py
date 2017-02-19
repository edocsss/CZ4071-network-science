from graph.util import data_util, plot_util
from graph.analyzer import clustering_coefficient_analyzer
from graph.analyzer import degree_analyzer
import pandas as pd
import numpy as np


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

    plot_util.plot_scatter(x, y, title='Log-Log Clustering Coefficient', x_label='k', y_label='C(k)', log_log=False)


def main():
    network = data_util.get_network()
    # print 'Average Clustering Coefficient:', clustering_coefficient_analyzer.calculate_average_clustering_coefficient(network)
    # print 'Global Clustering Coefficient:', clustering_coefficient_analyzer.calculate_global_clustering_coefficient(network)
    plot_clustering_coefficient_distribution(network)


if __name__ == '__main__':
    main()