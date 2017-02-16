import math
from graph_tool.draw import sfdp_layout


def _scale_node_degree(k, kmax, kmin):
    temp = int(((k - kmin) / float((kmax - kmin))) * 10)
    if temp == 0:
        temp += 1

    return math.pow(temp, 2)

def _get_sfdp_layout(network):
    return sfdp_layout(network)


def convert_gt_network_to_gui_format(network, kmax, kmin):
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
            'color': '#FF0000'
        })

    for i, e in enumerate(network.edges()):
        result['edges'].append({
            'id': 'e' + str(i),
            'source': 'v' + str(int(e.source())),
            'target': 'v' + str(int(e.target())),
            'size': 0,
            'color': '#000000'
        })

    return result
