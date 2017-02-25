from graph.analyzer import degree_analyzer, scale_free_network_analyzer
from graph.util import data_util


def main():
    network = data_util.get_network()
    degree_count = degree_analyzer.count_degree(network)
    degree_distribution = degree_analyzer.calculate_degree_distribution(degree_count)

    degree_exponent = scale_free_network_analyzer.calculate_real_degree_exponent(degree_count, plot=True)
    real_kmax = degree_analyzer.find_largest_degree(degree_distribution)
    real_kmin = degree_analyzer.find_smallest_degree(degree_distribution)

    print 'Degree Exponent (gamma):', degree_exponent
    print 'Expected degree exponent:', scale_free_network_analyzer.calculate_expected_degree_exponent(
        network.num_vertices(),
        real_kmax,
        real_kmin
    )


if __name__ == '__main__':
    main()
