import os
import uuid
from flask import request, Blueprint, jsonify, send_from_directory
import graph_tool as gt
from graph.analyzer import degree_analyzer
from graph.analyzer import distance_analyzer
from graph.analyzer import scale_free_network_analyzer
from graph.analyzer import clustering_coefficient_analyzer
from graph.analyzer import random_network_analyzer
from graph.util import network_format_converter
from graph.generator import random_network_generator
import config as CONFIG


blueprint = Blueprint('graph_handler', __name__)


@blueprint.route('/api/network', methods=['POST'])
def handle_graph():
    f = request.files['file']
    network_name = f.filename.split('.')[0]
    graph_csv = f.read()

    _store_graph_csv_to_file_system(network_name, graph_csv)
    result = _analyze_real_network_properties(network_name)
    return jsonify(result)


@blueprint.route('/api/network', methods=['GET'])
def handle_example_graph():
    network_name = 'sample_network'
    result = _analyze_real_network_properties(network_name)
    return jsonify(result)


@blueprint.route('/api/random_network', methods=['POST'])
def handle_random_network():
    json = request.get_json()
    n = json['n']
    p = json['p']

    result = _analyze_random_network_properties(n, p)
    return jsonify(result)


@blueprint.route('/api/img/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(CONFIG.DB_PLOT_DIR_PATH, filename)


def _analyze_real_network_properties(network_name):
    network = _load_graph_csv_from_file_system(network_name)
    is_too_big = _is_network_too_big(network.num_vertices(), network.num_edges())

    analyzed_network_properties = _compute_real_network_properties(network_name, network)
    theoretical_scale_free_network_properties = _compute_scale_free_properties(network)
    gui_network_format = network_format_converter.convert_gt_network_to_gui_format(
        network,
        network_name,
        analyzed_network_properties['real_kmax'],
        analyzed_network_properties['real_kmin'],
        use_image=is_too_big
    )

    return {
        'isTooBig': is_too_big,
        'guiNetworkFormat': gui_network_format,
        'analyzedNetworkProperties': analyzed_network_properties,
        'theoreticalScaleFreeNetworkProperties': theoretical_scale_free_network_properties
    }


def _analyze_random_network_properties(n, p):
    network = random_network_generator.generate_random_network(n, p)
    network_name = str(uuid.uuid4())
    is_too_big = _is_network_too_big(network.num_vertices(), network.num_edges())

    analyzed_network_properties = _compute_real_network_properties(network_name, network)
    theoretical_random_network_properties = _compute_random_network_properties(network.num_vertices(), p)

    gui_network_format = network_format_converter.convert_gt_network_to_gui_format(
        network,
        network_name,
        analyzed_network_properties['real_kmax'],
        analyzed_network_properties['real_kmin'],
        use_image=is_too_big
    )

    return {
        'isTooBig': is_too_big,
        'guiNetworkFormat': gui_network_format,
        'analyzedNetworkProperties': analyzed_network_properties,
        'theoreticalRandomNetworkProperties': theoretical_random_network_properties
    }


def _compute_real_network_properties(network_name, network):
    no_of_nodes = network.num_vertices()
    no_of_edges = network.num_edges()

    # Real Network Properties
    degree_count = degree_analyzer.count_degree(network)
    degree_distribution = degree_analyzer.calculate_degree_distribution(degree_count)
    degree_prob_distribution_plot_url = degree_analyzer.plot_and_store_degree_prob_distribution(network_name, degree_count)
    average_degree = degree_analyzer.calculate_degree_moment(degree_count, n=1)
    degree_second_moment = degree_analyzer.calculate_degree_moment(degree_count, n=2)
    real_kmax = degree_analyzer.find_largest_degree(degree_distribution)
    real_kmin = degree_analyzer.find_smallest_degree(degree_distribution)

    global_clustering_coefficient = clustering_coefficient_analyzer.calculate_global_clustering_coefficient(network)
    average_clustering_coefficient = clustering_coefficient_analyzer.calculate_average_clustering_coefficient(network)

    distance_distribution = distance_analyzer.get_distance_distribution(network)
    distance_prob_distribution_plot_file_name = distance_analyzer.plot_and_store_distance_prob_distribution(network_name, distance_distribution)
    average_distance = distance_analyzer.calculate_average_distance(no_of_nodes, distance_distribution)
    diameter = distance_analyzer.find_network_diameter(distance_distribution)

    return {
        'no_of_nodes': no_of_nodes,
        'no_of_edges': no_of_edges,
        'degree_prob_distribution_plot_file_name': degree_prob_distribution_plot_url,
        'average_degree': average_degree,
        'degree_second_moment': degree_second_moment,
        'real_kmax': real_kmax,
        'real_kmin': real_kmin,
        'distance_prob_distribution_plot_file_name': distance_prob_distribution_plot_file_name,
        'average_distance': average_distance,
        'diameter': diameter,
        'global_clustering_coefficient': global_clustering_coefficient,
        'average_clustering_coefficient': average_clustering_coefficient
    }


def _compute_scale_free_properties(network):
    no_of_nodes = network.num_vertices()
    degree_count = degree_analyzer.count_degree(network)
    degree_distribution = degree_analyzer.calculate_degree_distribution(degree_count)
    real_kmax = degree_analyzer.find_largest_degree(degree_distribution)
    real_kmin = degree_analyzer.find_smallest_degree(degree_distribution)

    degree_exponent = scale_free_network_analyzer.calculate_real_degree_exponent(degree_count)
    expected_kmax = scale_free_network_analyzer.calculate_expected_max_degree(no_of_nodes, real_kmin, degree_exponent)
    expected_average_distance = scale_free_network_analyzer.calculate_expected_average_distance(no_of_nodes, degree_exponent)
    expected_degree_exponent = scale_free_network_analyzer.calculate_expected_degree_exponent(no_of_nodes, real_kmax, real_kmin)

    return {
        'degree_exponent': degree_exponent,
        'expected_kmax': expected_kmax,
        'expected_average_distance': expected_average_distance,
        'expected_degree_exponent': expected_degree_exponent
    }


def _store_graph_csv_to_file_system(graph_name, graph_csv):
    f = open(os.path.join(CONFIG.DB_NETWORK_DIR_PATH, graph_name + '.csv'), 'w')
    f.write(graph_csv)
    f.close()


def _load_graph_csv_from_file_system(graph_name):
    f = open(os.path.join(CONFIG.DB_NETWORK_DIR_PATH, graph_name + '.csv'), 'r')
    network = gt.load_graph_from_csv(file_name=f, directed=False, csv_options={'delimiter': '\t'})
    f.close()

    return network


def _compute_random_network_properties(n, p):
    expected_no_of_edges = random_network_analyzer.calculate_no_of_edges(n, p)
    expected_average_degree = random_network_analyzer.calculate_average_degree(n, p)
    expected_degree_distribution = random_network_analyzer.calculate_degree_prob_distribution(n, p)
    expected_regime_type = random_network_analyzer.get_regime_type(n, p)

    expected_average_distance = random_network_analyzer.calculate_average_distance(n, p)
    expected_clustering_coefficient = random_network_analyzer.calculate_clustering_coefficient(p)

    return {
        'p': p,
        'expected_no_of_nodes': n,
        'expected_no_of_edges': expected_no_of_edges,
        'expected_degree_distribution': expected_degree_distribution,
        'expected_average_degree': expected_average_degree,
        'expected_regime_type': expected_regime_type,
        'expected_average_distance': expected_average_distance,
        'expected_clustering_coefficient': expected_clustering_coefficient
    }


def _is_network_too_big(no_of_nodes, no_of_edges):
    return no_of_nodes > 10000 or no_of_edges > 500000