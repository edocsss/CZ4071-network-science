from graph.util import network_util, random_network_util
from flask import request, Blueprint
import graph_tool as gt
import config as CONFIG
import os


blueprint = Blueprint('random_network_handler', __name__)


@blueprint.route('/random', methods=['POST'])
def handle_random_network():
    json = request.get_json()
    n = json['n']
    p = json['p']

    result = _compute_random_network_properties(n, p)
    return result


def _compute_random_network_properties(n, p):
    # Real random network
    random_network = random_network_util.generate_random_network(n, p)
    no_of_edges = random_network.num_edges()

    # Calculated using random network theory
    average_degree = random_network_util.calculate_average_degree(n)
    degree_distribution = random_network_util.get_degree_distribution(n)
    regime_type = random_network_util.get_regime_type(n)

    average_distance = random_network_util.calculate_average_distance(n)
    clustering_coefficient = random_network_util.calculate_clustering_coefficient(n)

    return {
        'no_of_nodes': n,
        'p': p,
        'no_of_edges': no_of_edges,
        'degree_distribution': degree_distri bution,
        'average_degree': average_degree,
        'regime_type': regime_type,
        'average_distance': average_distance,
        'clustering_coefficient': clustering_coefficient
    }
