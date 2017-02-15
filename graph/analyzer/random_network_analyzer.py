import math
from scipy.misc import factorial, comb
import numpy as np


def calculate_average_degree(n, p=0.05):
    return p * (n - 1)


def calculate_average_distance(n, p=0.05):
    avg_degree = calculate_average_degree(n, p)
    return math.log(n) / math.log(avg_degree)


def calculate_clustering_coefficient(p=0.05):
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
