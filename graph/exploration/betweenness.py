from graph_tool import centrality
# from graph.util import data_util
import os
import cPickle
import config as CONFIG


def analyze_betweenness(_network):
    vb, eb = centrality.betweenness(_network)

    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'vertex_betweenness.pkl')
    f = open(file_path, 'wb')
    cPickle.dump(vb.get_array(), f, cPickle.HIGHEST_PROTOCOL)
    f.close()


def read_betweenness_result():
    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, 'vertex_betweenness.pkl')
    f = open(file_path, 'rb')
    vb = cPickle.load(f)
    f.close()

    return vb


if __name__ == '__main__':
    # network = data_util.get_network()
    print(len(read_betweenness_result()))