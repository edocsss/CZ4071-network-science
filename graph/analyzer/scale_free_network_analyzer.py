from graph.util import plot_util
from scipy.stats import linregress
import math
import matplotlib.pyplot as plt


def calculate_real_degree_exponent(degree_count, plot=False):
    n, bins = plot_util.log_binning(degree_count, n_bins=50)
    bin_centers = list((bins[1:] + bins[:-1]) / 2)
    n = list(n)

    x_log, y_log = plot_util.get_log_log_points(bin_centers, n)
    slope, intercept, _, _, _ = linregress(x_log, y_log)

    if math.isnan(slope):
        return None

    xl = [math.log10(i) for i in range(1, 10000)]
    yl = [slope * math.log10(i) + intercept for i in range(1, 10000)]

    if plot:
        plt.plot(xl, yl, 'r')
        plot_util.plot_scatter(
            bin_centers,
            n,
            title='Log-Log Degree Distribution',
            x_label='k',
            y_label='P(k)',
            log_log=True
        )

    return -slope


def calculate_expected_max_degree(n, min_degree, degree_exponent):
    if degree_exponent is None:
        return None

    return min_degree * math.pow(n, 1 / (degree_exponent - 1))


def calculate_expected_average_distance(no_of_nodes, degree_exponent):
    if degree_exponent is None or degree_exponent < 2:
        return None
    elif degree_exponent == 2:
        return 'It\'s a constant'
    elif 2 < degree_exponent < 3:
        return math.log(math.log(no_of_nodes)) / math.log(degree_exponent - 1)
    elif degree_exponent == 3:
        return math.log(no_of_nodes) / math.log(math.log(no_of_nodes))
    else:
        return math.log(no_of_nodes)


def calculate_expected_degree_exponent(no_of_nodes, kmax, kmin):
    try:
        return (math.log(no_of_nodes) / math.log(kmax / kmin)) + 1

    except ZeroDivisionError:
        return None
