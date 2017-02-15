from graph.util import plot_util
from scipy.stats import linregress
import math
import matplotlib.pyplot as plt


def calculate_degree_exponent(degree_count, plot=False):
    n, bins = plot_util.log_binning(degree_count, n_bins=50)
    bin_centers = list((bins[1:] + bins[:-1]) / 2)
    n = list(n)

    x_log, y_log = plot_util.get_log_log_points(bin_centers, n)
    slope, intercept, _, _, _ = linregress(x_log, y_log)

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

    return slope