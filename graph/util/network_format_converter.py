import math
import os
from graph_tool.draw import sfdp_layout, graph_draw
import config as CONFIG


def _scale_node_degree(k, kmax, kmin):
    if (kmax - kmin > 0):
        temp = int(((k - kmin) / float((kmax - kmin)) + 1) * 2)

    return math.pow(temp, 2)


def _get_sfdp_layout(network):
    return sfdp_layout(network)


def _convert_network_to_json_format(network, kmax, kmin):
    result = {
        'nodes': [],
        'edges': []
    }

    layout = _get_sfdp_layout(network)
    for v in network.vertices():
        v_id = int(v)
        result['nodes'].append({
            'id': 'v' + str(v_id),
            'x': layout[v][0],
            'y': layout[v][1],
            'size': _scale_node_degree(v.out_degree(), kmax, kmin),
            'color': '#E91E63'
        })

    for i, e in enumerate(network.edges()):
        result['edges'].append({
            'id': 'e' + str(i),
            'source': 'v' + str(int(e.source())),
            'target': 'v' + str(int(e.target())),
            'size': 0,
            'color': '#424242'
        })

    return result


def _plot_network_and_save_as_image(network, network_name):
    file_name = network_name + '.png'
    file_path = os.path.join(CONFIG.DB_PLOT_DIR_PATH, file_name)

    layout = _get_sfdp_layout(network)
    graph_draw(network, pos=layout, output=file_path)
    return file_name


def convert_gt_network_to_gui_format(network, network_name, kmax, kmin, use_image=False):
    if not use_image:
        return _convert_network_to_json_format(network, kmax, kmin)
    else:
        return _plot_network_and_save_as_image(network, network_name)
