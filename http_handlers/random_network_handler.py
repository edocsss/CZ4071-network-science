from flask import request, Blueprint
from graph.analyzer import random_network_analyzer
from graph.generator import random_network_generator


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
    network = random_network_generator.generate_random_network(n, p)
    no_of_edges = network.num_edges()

    # Calculated using random network theory
    average_degree = random_network_analyzer.calculate_average_degree(n)
    degree_distribution = random_network_analyzer.get_degree_distribution(n)
    regime_type = random_network_analyzer.get_regime_type(n)

    average_distance = random_network_analyzer.calculate_average_distance(n)
    clustering_coefficient = random_network_analyzer.calculate_clustering_coefficient(n)

    return {
        'no_of_nodes': n,
        'p': p,
        'no_of_edges': no_of_edges,
        'degree_distribution': degree_distribution,
        'average_degree': average_degree,
        'regime_type': regime_type,
        'average_distance': average_distance,
        'clustering_coefficient': clustering_coefficient
    }
