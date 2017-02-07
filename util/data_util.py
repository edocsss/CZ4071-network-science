import config as CONFIG
import graph_tool as gt
import os
import graph_tool.clustering as gt_clustering
import graph_tool.stats as gt_stats
import cPickle
import gc


def _read_network(file_name='google_network_raw.csv', replace_pickle=False):
    file_path = os.path.join(CONFIG.DATA_DIR_PATH, file_name)
    pickle_name = file_name.split('.')[0] + '.p'
    pickle_path = os.path.join(CONFIG.DATA_DIR_PATH, pickle_name)

    if os.path.isfile(pickle_path) and not replace_pickle:
        print 'Test'
        return _load_network()

    f = open(file_path, 'r')
    G = gt.load_graph_from_csv(file_name=f, directed=True, csv_options={'delimiter': '\t'})
    f.close()

    _store_network(G)
    return G


def _store_network(network, file_name='google_network_raw.p'):
    file_path = os.path.join(CONFIG.DATA_DIR_PATH, file_name)
    f = open(file_path, 'wb')

    gc.disable()
    cPickle.dump(network, f, protocol=cPickle.HIGHEST_PROTOCOL)
    gc.enable()

    f.close()


def _load_network(file_name='google_network_raw.p'):
    file_path = os.path.join(CONFIG.DATA_DIR_PATH, file_name)
    f = open(file_path, 'rb')

    gc.disable()
    network = cPickle.load(f)
    gc.enable()

    f.close()
    return network


def get_network():
    return _network


_network = _read_network(file_name='google_network_raw.csv', replace_pickle=False)


if __name__ == '__main__':
    network = get_network()
    print network.num_vertices()
    print network.num_edges()

    # import time
    # start = time.time()
    # print gt_clustering.local_clustering(network, undirected=False)
    # print 'Time 1:', time.time() - start
    #
    # start = time.time()
    # print gt_clustering.global_clustering(network)
    # print 'Time 2:', time.time() - start
    #
    # start = time.time()
    # print gt_stats.distance_histogram(network)
    # print 'Time 3:', time.time() - start
