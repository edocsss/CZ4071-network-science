import math
import os
import matplotlib.pyplot as plt
from graph.util import plot_util
import config as CONFIG


def count_degree(network):
    counter = {}
    for v in network.vertices():
        vertex_id = int(v)
        counter[vertex_id] = v.out_degree()

    return counter


def calculate_degree_distribution(degree_count):
    degree_distribution = {}
    for k, v in degree_count.items():
        if v not in degree_distribution:
            degree_distribution[v] = 0

        degree_distribution[v] += 1

    return degree_distribution


def calculate_degree_prob_distribution(no_of_nodes, degree_distribution):
    for k, v in degree_distribution.items():
        degree_distribution[k] = float(v) / no_of_nodes

    return degree_distribution


def plot_and_store_degree_prob_distribution(network_name, degree_count):
    file_name = network_name + '_degree_distribution_log_binning.png'
    file_path = os.path.join(CONFIG.DB_PLOT_DIR_PATH, file_name)

    n, bins = plot_util.log_binning(degree_count, n_bins=50, plot=False)
    bin_centers = list((bins[1:] + bins[:-1]) / 2)
    n = list(n)

    x_log, y_log = plot_util.get_log_log_points(bin_centers, n)
    plt.scatter(x_log, y_log, s=2, c='r')
    plt.title('Log-Log Degree Distribution with Log Binning')
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.savefig(file_path)
    plt.close()

    return file_name


def calculate_degree_moment(degree_count, n=1):
    return sum([
        math.pow(c, n) for c in degree_count.values()
    ]) / len(degree_count.values())


def find_largest_degree(degree_distribution):
    return max(degree_distribution.keys())


def find_smallest_degree(degree_distribution):
    return min(degree_distribution.keys())