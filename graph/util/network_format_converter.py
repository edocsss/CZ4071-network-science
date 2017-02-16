def convert_gt_network_to_gui_format(network):
    result = {
        'nodes': [],
        'links': []
    }

    for v in network.vertices():
        v_id = int(v)
        result['nodes'].append({
            'id': v_id
        })

    for e in network.edges():
        result['links'].append({
            'source': int(e.source()),
            'target': int(e.target())
        })

    return result