import os
import math
import numpy as np
import matplotlib.pyplot as plt
from graph.util import plot_util
import config as CONFIG


def calculate_no_of_edges(n, p):
    return p * (n * (n - 1) / 2)


def calculate_average_degree(n, p=0.05):
    return p * (n - 1)


def calculate_average_distance(n, p=0.05):
    avg_degree = calculate_average_degree(n, p)
    return math.log(n) / math.log(avg_degree)


def calculate_clustering_coefficient(p=0.05):
    return p


def calculate_degree_prob_distribution(network_name, n, p=0.05):
    avg_degree = calculate_average_degree(n, p)
    size = 10000

    if n >= 1000:
        vals = np.random.poisson(avg_degree, size)
    else:
        vals = np.random.binomial(n, p, size)

    file_name = network_name + '_theoretical_degree_distribution_log_binning.png'
    file_path = os.path.join(CONFIG.DB_PLOT_DIR_PATH, file_name)

    x = np.sort(vals)
    unique = np.unique(x)

    log_bins = np.logspace(math.log10(min(x)) if min(x) > 0 else math.log10(unique[1]), math.log10(max(x)), 50)
    y, bins, _ = plt.hist(x, bins=log_bins, log=True, normed=True)
    bin_centers = list((bins[1:] + bins[:-1]) / 2)
    y = list(y)

    x_log, y_log = plot_util.get_log_log_points(bin_centers, y)
    plt.clf()
    plt.scatter(x_log, y_log, s=2, c='r')
    plt.title('Log-Log Theoretical Degree Distribution with Log Binning')
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.savefig(file_path)
    plt.close()

    return file_name


def get_regime_type(n, p=0.05):
    avg_degree = calculate_average_degree(n, p)
    if avg_degree < 1:
        return 'subcritical'
    elif avg_degree == 1:
        return 'critical'
    elif avg_degree > math.log(n):
        return 'connected'
    elif avg_degree > 1:
        return 'supercritical'
