from scipy.misc import factorial, comb
import graph_tool as gt
import graph_tool.topology as gtt
import math
import subprocess
import numpy as np
import config as CONFIG
import os


def calculate_average_degree(n, p=0.05):
    return p * (n - 1)


def calculate_average_distance(n, p=0.05):
    avg_degree = calculate_average_degree(n, p)
    return math.log(n) / math.log(avg_degree)


def calculate_clustering_coefficient(n, p=0.05):
    return p


def get_degree_distribution(n, p=0.05):
    avg_degree = calculate_average_degree(n, p)

    def _calculate_poisson_prob(k):
        return math.pow(math.e, -avg_degree) * (math.pow(avg_degree, k) / factorial(k))

    def _calculate_binomial_prob(k):
        return comb(n - 1, k) * math.pow(p, k) * math.pow(1 - p, n - 1 - k)

    k_values = np.array([k for k in range(2 * avg_degree)])
    prob_func = _calculate_poisson_prob if n >= 1000 else _calculate_binomial_prob
    return np.apply_along_axis(func1d=prob_func, axis=0, arr=k_values).tolist()


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


def generate_random_network(n, p=0.05):
    subprocess.Popen(["./random_graph_generator", str(n), str(p)], stdout=subprocess.PIPE).communicate()[0].decode().strip()
    temp_file_path = os.path.join(CONFIG.GRAPH_DIR_PATH, 'util', 'temp.csv')

    f = open(temp_file_path, 'r')
    random_network = gt.load_graph_from_csv(file_name=f, directed=False, csv_options={'delimiter': '\t'})
    f.close()

    os.remove(temp_file_path)
    return random_network