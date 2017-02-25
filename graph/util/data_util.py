import os
import cPickle
import gc
import graph_tool as gt
import config as CONFIG


def _read_network(file_name='raw.csv', replace_pickle=False):
    file_path = os.path.join(CONFIG.DATA_DIR_PATH, file_name)
    pickle_name = file_name.split('.')[0] + '.pkl'
    pickle_path = os.path.join(CONFIG.DATA_DIR_PATH, pickle_name)

    if os.path.isfile(pickle_path) and not replace_pickle:
        print 'Reading graph from pickle..'
        return load_network()

    f = open(file_path, 'r')
    print 'Loading graph from raw file...'
    G = gt.load_graph_from_csv(
        file_name=f,
        directed=False,
        csv_options={'delimiter': '\t'}
    )

    f.close()

    print 'storing graph...'
    store_network(G, file_name=pickle_name)

    return G


def store_network(network, file_name='raw.pkl'):
    file_path = os.path.join(CONFIG.DATA_DIR_PATH, file_name)
    f = open(file_path, 'wb')
    gc.disable()
    cPickle.dump(network, f)
    gc.enable()
    f.close()


def load_network(file_name='raw.pkl'):
    file_path = os.path.join(CONFIG.DATA_DIR_PATH, file_name)
    f = open(file_path, 'rb')
    gc.disable()
    network = cPickle.load(f)
    gc.enable()
    f.close()
    return network


def get_network():
    return _read_network(file_name='raw.csv', replace_pickle=False)