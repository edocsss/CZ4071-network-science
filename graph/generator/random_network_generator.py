import os
import subprocess
import graph_tool as gt
import config as CONFIG
from graph_tool.generation import price_network
from graph_tool.draw import graph_draw, sfdp_layout


def generate_random_network(n, p=0.05):
    generator_path = os.path.join(
        CONFIG.GRAPH_DIR_PATH,
        'generator',
        'random_graph_generator'
    )

    subprocess.Popen(
        [generator_path, str(n), str(p)],
        stdout=subprocess.PIPE
    ).communicate()[0].decode().strip()

    temp_file_path = os.path.join(
        os.getcwd(),
        'temp.csv'
    )

    f = open(temp_file_path, 'r')
    random_network = gt.load_graph_from_csv(
        file_name=f,
        directed=False,
        csv_options={'delimiter': '\t'}
    )
    f.close()

    os.remove(temp_file_path)
    return random_network


if __name__ == '__main__':
    import time
    network = price_network(5000, m=2, directed=False)

    start = time.time()
    layout = sfdp_layout(network)
    graph_draw(network, pos=layout, output='price.png')
    print time.time() - start