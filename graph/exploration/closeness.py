from graph_tool import centrality
from graph.util import data_util
import os
import cPickle
import config as CONFIG


def analyze_closeness(_network):
    closeness = centrality.closeness(_network)

    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'closeness.pkl')
    f = open(file_path, 'wb')
    cPickle.dump(closeness, f, cPickle.HIGHEST_PROTOCOL)
    f.close()


if __name__ == '__main__':
    network = data_util.get_network()
    analyze_closeness(network)
