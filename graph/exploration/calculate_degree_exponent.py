from graph.analyzer import degree_analyzer, scale_free_network_analyzer
from graph.util import data_util


def main():
    network = data_util.get_network()
    degree_count = degree_analyzer.count_degree(network)

    degree_exponent = scale_free_network_analyzer.calculate_degree_exponent(degree_count)
    print 'Degree Exponent (gamma):', degree_exponent


if __name__ == '__main__':
    main()
