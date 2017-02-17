from graph.util import data_util
from graph_tool.draw import sfdp_layout, graph_draw
import os
import config as CONFIG
import time


def visualize_graph(network, file_name):
    file_path = os.path.join(CONFIG.RESULTS_DIR_PATH, file_name)
    layout = sfdp_layout(network)
    graph_draw(network, pos=layout, output=file_path)


if __name__ == '__main__':
    network = data_util.get_network()
    print 'Start!'
    start = time.time()
    visualize_graph(network, 'youtube_full_network.png')
    print time.time() - start
    print 'Stop!'
