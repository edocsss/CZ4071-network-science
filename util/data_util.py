import config as CONFIG
import graph_tool as gt
import os
import graph_tool.clustering as gt_clustering
import graph_tool.stats as gt_stats


def _read_network(file_name='google_network_raw.csv'):
    file_path = os.path.join(CONFIG.DATA_DIR_PATH, file_name)
    f = open(file_path, 'r')
    G = gt.load_graph_from_csv(file_name=f, directed=True, csv_options={'delimiter': '\t'})
    f.close()

    return G


def get_network():
    return _network


_network = _read_network(file_name='google_network_raw.csv')


if __name__ == '__main__':
    network = get_network()
    print network.num_vertices()
    print network.num_edges()

    import time
    start = time.time()
    print gt_clustering.local_clustering(network, undirected=False)
    print 'Time 1:', time.time() - start

    start = time.time()
    print gt_clustering.global_clustering(network)
    print 'Time 2:', time.time() - start

    start = time.time()
    print gt_stats.distance_histogram(network)
    print 'Time 3:', time.time() - start
