import graph_tool as gt
import graph_tool.draw as gt_draw
import argparse

CAIRO = 'cairo'
GRAPHVIZ = 'graphviz'
WIDGET = 'widget'
WINDOW = 'window'
INTERACTIVE_WINDOW = 'interactive'

def load_graph(file_path):
    return gt.load_graph_from_csv(file_path, directed=False, skip_first=True)


def plot_graph(G, opt='cairo'):
    if opt == CAIRO:
        gt_draw.graph_draw(G)
    elif opt == GRAPHVIZ:
        gt_draw.graphviz_draw(G)
    elif opt == WIDGET or opt == WINDOW:
        pos, selected = gt.draw.interactive_window(G)
        if opt == WIDGET:
            gt_draw.GraphWidget(G, pos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--show', help='Draw the graph visualization', action='store_true')
    parser.add_argument('-f', '--file', default='static/data/youtube_graph.txt', help='File input path')
    parser.add_argument('-t', '--type', default='cairo', help='Visualization method: cairo, graphviz, widget, window')
    args = parser.parse_args()
    
    G = load_graph(args.file)
    if args.show:
        plot_graph(G, args.type)