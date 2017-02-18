from graph.util import data_util
from graph.analyzer import clustering_coefficient_analyzer


def main():
    network = data_util.get_network()
    print 'Average Clustering Coefficient:', clustering_coefficient_analyzer.calculate_average_clustering_coefficient(network)
    print 'Global Clustering Coefficient:', clustering_coefficient_analyzer.calculate_global_clustering_coefficient(network)


if __name__ == '__main__':
    main()