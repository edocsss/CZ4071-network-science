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


    pass