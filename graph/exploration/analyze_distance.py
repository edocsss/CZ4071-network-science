import os
import cPickle
from graph.analyzer import distance_analyzer
from graph.util import data_util
import config as CONFIG


def _read_stored_distance_distributions():
    files = os.listdir(os.path.join(CONFIG.RESULTS_DIR_PATH, 'shortest_distance'))
    distance_distributions = []

    for file_name in files:
        if file_name.startswith('shortest_distance_result_'):
            file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'shortest_distance', file_name)
            f = open(file_path, 'rb')
            distance_distributions.append(cPickle.load(f))
            f.close()

    return distance_distributions


def main():
    network = data_util.get_network()
    no_of_nodes = network.num_vertices()

    distance_distributions = _read_stored_distance_distributions()
    combined_distance_distribution = distance_analyzer.combine_multiple_distance_distributions(distance_distributions)
    distance_prob_distribution = distance_analyzer.calculate_distance_prob_distribution(combined_distance_distribution)

    print 'Average Distance:', distance_analyzer.calculate_average_distance(no_of_nodes, combined_distance_distribution)
    print 'Diameter:', distance_analyzer.find_network_diameter(combined_distance_distribution)
    print distance_analyzer.plot_and_store_distance_prob_distribution('youtube', distance_prob_distribution)


if __name__ == '__main__':
    main()


    