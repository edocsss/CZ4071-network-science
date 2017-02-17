from graph.util import data_util
from graph_tool.draw import sfdp_layout, graph_draw
import graph_tool as gt
import os
from multiprocessing import Process
import config as CONFIG
import time


def visualize_graph(network, file_name):
    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, file_name)
    layout = sfdp_layout(network)
    graph_draw(network, pos=layout, output=file_path)


def get_node_with_max_degree(network):
    max_degree = -1
    max_index = -1

    for v in network.vertices():
        v_degree = v.out_degree()
        if v_degree > max_degree:
            max_degree = v_degree
            max_index = int(v)

    return max_index


def get_subgraph_with_n_nodes(network, max_n, max_edge_per_vertex=5000):
    no_of_vertices = network.num_vertices()
    max_vid = get_node_with_max_degree(network)

    visited = {max_vid}
    v_list = [max_vid]
    e_list = []
    current_index = 0

    print 'Starting traversal'
    while current_index < no_of_vertices and len(v_list) < max_n:
        edge_counter = 0
        current_vid = v_list[current_index]
        current_v = network.vertex(current_vid)

        for e in current_v.all_edges():
            next_vid = int(e.target())

            if next_vid not in visited:
                visited.add(next_vid)
                v_list.append(next_vid)
                e_list.append((int(e.source()), int(e.target())))

                if len(v_list) >= max_n:
                    break

            if edge_counter > max_edge_per_vertex:
                break

            edge_counter += 1

        current_index += 1

    return generate_subgraph_from_network(e_list)


def generate_subgraph_from_network(edges):
    print 'Subgraph generation!'
    subgraph = gt.Graph(directed=False)
    v_props = subgraph.new_vertex_property('bool')

    for e in edges:
        subgraph.add_edge(e[0], e[1], add_missing=True)

    for v in subgraph.vertices():
        if not v.is_valid() or v.out_degree() == 0:
            v_props[v] = False
        else:
            v_props[v] = True

    subgraph.set_vertex_filter(v_props)
    return subgraph


def main(network, n, e):
    start = time.time()
    subgraph = get_subgraph_with_n_nodes(network, max_n=max_n, max_edge_per_vertex=max_edge_per_vertex)
    print time.time() - start

    start = time.time()
    file_name = 'youtube_n_{}_e_{}.png'.format(max_n, max_edge_per_vertex)
    visualize_graph(subgraph, file_name)
    print time.time() - start



if __name__ == '__main__':
    network = data_util.get_network()
    for max_n in [100, 500, 1000, 5000, 7500, 10000, 50000, 100000]:
        processes = []
        for max_edge_per_vertex in [100, 300, 500, 1000, 5000]:
            p = Process(target=main, args=(network, max_n, max_edge_per_vertex,))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()