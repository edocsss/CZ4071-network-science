from graph.util import network_util, random_network_util
from flask import request, Blueprint
import graph_tool as gt
import config as CONFIG
import os


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
        'real_network_properties': _compute_real_network_properties(network),
        'random_network_properties': _compute_random_network_properties(network),
        'scale_free_network_properties': _compute_scale_free_network_properties(network)
    }

    return result


def _compute_real_network_properties(network):
    no_of_nodes = network.num_vertices()
    no_of_edges = network.num_edges()

    degree_count = network_util.count_degree(network)
    degree_distribution = network_util.analyze_degree_distribution(degree_count)

    average_degree = network_util.calculate_moment(degree_count, n=1)
    degree_second_moment = network_util.calculate_moment(degree_count, n=2)

    global_clustering_coefficient = network_util.calculate_global_clustering_coefficient(network)
    average_clustering_coefficient = network_util.calculate_average_clustering_coefficient(network)

    return {
        'no_of_nodes': no_of_nodes,
        'no_of_edges': no_of_edges,
        'degree_distribution': degree_distribution,
        'average_degree': average_degree,
        'degree_second_moment': degree_second_moment,
        'shortest_distance_distribution': None,
        'average_distance': None,
        'diameter': None,
        'global_clustering_coefficient': global_clustering_coefficient,
        'average_clustering_coefficient': average_clustering_coefficient,
    }


# All formulas!
def _compute_random_network_properties(network):
    no_of_nodes = network.num_vertices()
    no_of_edges = network.num_edges()

    average_degree = random_network_util.calculate_average_degree(no_of_nodes)
    degree_distribution = random_network_util.get_degree_distribution(no_of_nodes)
    regime_type = random_network_util.get_regime_type(no_of_nodes)

    average_distance = random_network_util.calculate_average_distance(no_of_nodes)
    clustering_coefficient = random_network_util.calculate_clustering_coefficient(no_of_nodes)

    return {
        'no_of_nodes': no_of_nodes,
        'no_of_edges': no_of_edges,
        'degree_distribution': degree_distribution,
        'average_degree': average_degree,
        'regime_type': regime_type,
        'average_distance': average_distance,
        'clustering_coefficient': clustering_coefficient
    }


def _compute_scale_free_network_properties(network):
    pass


def _store_graph_csv_to_file_system(graph_name, graph_csv):
    f = open(os.path.join(CONFIG.DB_DIR_PATH, graph_name + '.csv'))
    f.write(graph_csv)
    f.close()


def _load_graph_csv_from_file_system(graph_name):
    f = open(os.path.join(CONFIG.DB_DIR_PATH, graph_name + '.csv'))
    network = gt.load_graph_from_csv(file_name=f, directed=False, csv_options={'delimiter': '\t'})
    f.close()

    return network
