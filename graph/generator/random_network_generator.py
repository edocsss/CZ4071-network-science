import os
import subprocess
import graph_tool as gt
import config as CONFIG


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
