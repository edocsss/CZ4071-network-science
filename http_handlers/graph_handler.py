import os
from flask import request, Blueprint
import graph_tool as gt
from graph.analyzer import degree_analyzer, distance_analyzer, scale_free_network_analyzer, clustering_coefficient_analyzer
from graph.util import network_format_converter
import config as CONFIG


blueprint = Blueprint('graph_handler', __name__)


@blueprint.route('/network', methods=['POST'])
def handle_graph():
    json = request.get_json()
    graph_csv = json['graphCsv']
    graph_name = json['graphName']

    # graph_csv is the CSV text!
    _store_graph_csv_to_file_system(graph_name, graph_csv)
    result = _compute_graph_properties(graph_name)
    return result


def _compute_graph_properties(graph_name):
    network = _load_graph_csv_from_file_system(graph_name)
    result = {
        'gui_network_format': network_format_converter.convert_gt_network_to_gui_format(network),
        'real_network_properties': _compute_real_network_properties(network),
        'scale_free_network_properties': _compute_scale_free_network_properties(network)
    }

    return result


def _compute_real_network_properties(network):
    no_of_nodes = network.num_vertices()
    no_of_edges = network.num_edges()

    degree_count = degree_analyzer.count_degree(network)
    degree_prob_distribution = degree_analyzer.analyze_degree_distribution(degree_count)

    average_degree = degree_analyzer.calculate_degree_moment(degree_count, n=1)
    degree_second_moment = degree_analyzer.calculate_degree_moment(degree_count, n=2)

    global_clustering_coefficient = clustering_coefficient_analyzer.calculate_global_clustering_coefficient(network)
    average_clustering_coefficient = clustering_coefficient_analyzer.calculate_average_clustering_coefficient(network)

    distance_distribution = distance_analyzer.get_distance_distribution(network)
    distance_prob_distribution = distance_analyzer.calculate_distance_prob_distribution(distance_distribution)
    average_distance = distance_analyzer.calculate_average_distance(no_of_nodes, distance_distribution)
    diameter = distance_analyzer.find_network_diameter(distance_distribution)

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
    }


def _compute_scale_free_network_properties(network):
    return {

    }


def _store_graph_csv_to_file_system(graph_name, graph_csv):
    f = open(os.path.join(CONFIG.DB_DIR_PATH, graph_name + '.csv'))
    f.write(graph_csv)
    f.close()


def _load_graph_csv_from_file_system(graph_name):
    f = open(os.path.join(CONFIG.DB_DIR_PATH, graph_name + '.csv'))
    network = gt.load_graph_from_csv(file_name=f, directed=False, csv_options={'delimiter': '\t'})
    f.close()

    return network
