import config as CONFIG
import networkx as nx
import os
import pickle


def _read_network(file_name='google_network_raw', replace_pickle=False):
    """
    This method will cache the resulting Graph in the form of a pickle file.
    The edges list file must be in a TXT file!!
    :param file_name: the network's edges list TXT file
    :return: graph representing the network
    """

    pickle_name = file_name + '.p'
    pickle_path = os.path.join(CONFIG.DATA_DIR_PATH, pickle_name)

    if os.path.isfile(pickle_path) and not replace_pickle:
        return _read_pickle_by_path(pickle_path)

    file_name_with_ext = file_name + '.txt'
    file_path = os.path.join(CONFIG.DATA_DIR_PATH, file_name_with_ext)

    G = nx.read_edgelist(file_path, create_using=nx.DiGraph())
    _write_pickle_to_path(pickle_path, G)

    return G


def _read_pickle_by_path(pickle_path):
    f = open(pickle_path, 'rb')
    obj = pickle.load(f)
    f.close()

    return obj


def _write_pickle_to_path(pickle_path, obj):
    f = open(pickle_path, 'wb')
    pickle.dump(obj, f)
    f.close()


def get_network():
    return _network


_network = _read_network(file_name='google_network_raw', replace_pickle=False)


if __name__ == '__main__':
    network = get_network()
    print(network.edges())
