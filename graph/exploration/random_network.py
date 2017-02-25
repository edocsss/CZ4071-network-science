import time
from graph.generator import random_network_generator
from graph.util import data_util


def _generate_random_network_and_store(n, p):
    network = random_network_generator.generate_random_network(n, p)
    data_util.store_network(network, 'random_network.pkl')


if __name__ == '__main__':
    start = time.time()
    _generate_random_network_and_store(n=1134890, p=0.0000046393)
    print time.time() - start