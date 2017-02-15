from graph.util import data_util, network_util


if __name__ == '__main__':
    network = data_util.get_network()
    degree_count = network_util.count_degree(network)

    degree_exponent = network_util.calculate_degree_exponent(degree_count)
    print 'Degree Exponent (gamma):', degree_exponent