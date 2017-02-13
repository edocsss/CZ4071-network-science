import os


ROOT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DB_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'db')

GRAPH_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'graph')
DATA_DIR_PATH = os.path.join(GRAPH_DIR_PATH, 'data')
RESULTS_DIR_PATH = os.path.join(GRAPH_DIR_PATH, 'results')