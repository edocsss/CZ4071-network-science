import math
from scipy.misc import factorial, comb


def calculate_no_of_edges(n, p):
    return p * (n * (n - 1) / 2)


def calculate_average_degree(n, p=0.05):
    return p * (n - 1)


def calculate_average_distance(n, p=0.05):
    avg_degree = calculate_average_degree(n, p)
    return math.log(n) / math.log(avg_degree)


def calculate_clustering_coefficient(p=0.05):
    return p


def calculate_degree_prob_distribution(n, p=0.05):
    avg_degree = calculate_average_degree(n, p)

    def _calculate_poisson_prob(k):
        return {
            k: math.pow(math.e, -avg_degree) * (math.pow(avg_degree, k) / factorial(k))
        }

    def _calculate_binomial_prob(k):
        return {
            k: comb(n - 1, k) * math.pow(p, k) * math.pow(1 - p, n - 1 - k)
        }

    k_values = [k for k in range(2 * int(avg_degree))]
    prob_func = _calculate_poisson_prob if n >= 1000 else _calculate_binomial_prob
    return map(prob_func, k_values)


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
