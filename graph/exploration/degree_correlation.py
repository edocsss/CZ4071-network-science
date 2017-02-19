from graph_tool import correlations
from graph.util import data_util
import os
import config as CONFIG
import matplotlib.pyplot as plt


def analyze_degree_correlation(_network):
    h = correlations.corr_hist(_network, deg_source='out', deg_target='out')
    plt.clf()

    plt.xlabel('Source Out-Degree')
    plt.ylabel('Target out-Degree')
    plt.imshow(h[0].T, interpolation='nearest', origin='lower')
    plt.colorbar()

    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'degree_correlation.png')
    plt.savefig(file_path)
    plt.close()


if __name__ == '__main__':
    network = data_util.get_network()
    analyze_degree_correlation(network)
