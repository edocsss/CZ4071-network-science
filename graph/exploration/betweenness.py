from graph_tool import centrality
from graph.util import data_util
import os
import cPickle
import config as CONFIG


def analyze_betweenness(_network):
    vb, eb = centrality.betweenness(_network)

    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'vertex_betweenness.pkl')
    f = open(file_path, 'wb')
    cPickle.dump(vb, f, cPickle.HIGHEST_PROTOCOL)
    f.close()

    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'edge_betweenness.pkl')
    f = open(file_path, 'wb')
    cPickle.dump(eb, f, cPickle.HIGHEST_PROTOCOL)
    f.close()


if __name__ == '__main__':
    network = data_util.get_network()
    analyze_betweenness(network)
