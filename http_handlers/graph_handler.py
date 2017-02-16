import os
from flask import request, Blueprint, jsonify
import graph_tool as gt
from graph.analyzer import degree_analyzer, distance_analyzer, scale_free_network_analyzer, clustering_coefficient_analyzer
from graph.util import network_format_converter
import config as CONFIG


blueprint = Blueprint('graph_handler', __name__)


@blueprint.route('/api/network', methods=['POST'])
def handle_graph():
    file = request.files['file']
    graph_name = file.filename.split('.')[0]
    graph_csv = file.read()

    # graph_csv is the CSV text!
    _store_graph_csv_to_file_system(graph_name, graph_csv)
    result = _compute_graph_properties(graph_name)
    return jsonify(result)


@blueprint.route('/api/network', methods=['GET'])
def handle_example_graph():
    graph_name = 'sample_network'
    result = _compute_graph_properties(graph_name)
    return jsonify(result)


def _compute_graph_properties(graph_name):
    network = _load_graph_csv_from_file_system(graph_name)
    result = {
        'guiNetworkFormat': network_format_converter.convert_gt_network_to_gui_format(network),
        'networkProperties': _compute_network_properties(network)
    }

    return result


def _compute_network_properties(network):
    no_of_nodes = network.num_vertices()
    no_of_edges = network.num_edges()

    # Real Network Properties
    degree_count = degree_analyzer.count_degree(network)
    degree_distribution = degree_analyzer.calculate_degree_distribution(degree_count)
    degree_prob_distribution = degree_analyzer.calculate_degree_prob_distribution(no_of_nodes, degree_distribution)
    average_degree = degree_analyzer.calculate_degree_moment(degree_count, n=1)
    degree_second_moment = degree_analyzer.calculate_degree_moment(degree_count, n=2)
    real_kmax = degree_analyzer.find_largest_degree(degree_distribution)
    real_kmin = degree_analyzer.find_smallest_degree(degree_distribution)

    global_clustering_coefficient = clustering_coefficient_analyzer.calculate_global_clustering_coefficient(network)
    average_clustering_coefficient = clustering_coefficient_analyzer.calculate_average_clustering_coefficient(network)

    distance_distribution = distance_analyzer.get_distance_distribution(network)
    distance_prob_distribution = distance_analyzer.calculate_distance_prob_distribution(distance_distribution)
    average_distance = distance_analyzer.calculate_average_distance(no_of_nodes, distance_distribution)
    diameter = distance_analyzer.find_network_diameter(distance_distribution)

    degree_exponent = scale_free_network_analyzer.calculate_real_degree_exponent(degree_count)


    # Scale Free Theoretical Value
    expected_kmax = scale_free_network_analyzer.calculate_expected_max_degree(no_of_nodes, real_kmin, degree_exponent)
    expected_average_distance = scale_free_network_analyzer.calculate_expected_average_distance(no_of_nodes, degree_exponent)
    expected_degree_exponent = scale_free_network_analyzer.calculate_expected_degree_exponent(no_of_nodes, real_kmax, real_kmin)

    return {
        'no_of_nodes': no_of_nodes,
        'no_of_edges': no_of_edges,
        'degree_prob_distribution': degree_prob_distribution,
        'average_degree': average_degree,
        'degree_second_moment': degree_second_moment,
        'shortest_distance_prob_distribution': distance_prob_distribution,
        'average_distance': average_distance,
        'diameter': diameter,
        'global_clustering_coefficient': global_clustering_coefficient,
        'average_clustering_coefficient': average_clustering_coefficient,
        'degree_exponent': degree_exponent,

        'expected_kmax': expected_kmax,
        'expected_average_distance': expected_average_distance,
        'expected_degree_exponent': expected_degree_exponent
    }


def _store_graph_csv_to_file_system(graph_name, graph_csv):
    f = open(os.path.join(CONFIG.DB_DIR_PATH, graph_name + '.csv'), 'w')
    f.write(graph_csv)
    f.close()


def _load_graph_csv_from_file_system(graph_name):
    f = open(os.path.join(CONFIG.DB_DIR_PATH, graph_name + '.csv'), 'r')
    network = gt.load_graph_from_csv(file_name=f, directed=False, csv_options={'delimiter': '\t'})
    f.close()

    return network


if __name__ == '__main__':
    print _compute_graph_properties('sample_network')
