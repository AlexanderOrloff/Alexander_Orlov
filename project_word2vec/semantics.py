import sys
import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt


m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
words = ['утка_NOUN', 'гусь_NOUN', 'селезень_NOUN', 'птица_NOUN', 'страус_NOUN']


def unpacking(m):
    if m.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
        model = gensim.models.KeyedVectors.load(m)
    model.init_sims(replace=True)
    return model

def graph_design(model, words):
    G = nx.Graph()
    G.add_nodes_from(words)
    for i in words:
        for j in words:
            if i !=j:
                if model.similarity(i, j) > 0.5:
                    G.add_edge(i,j )
    return G


def graph_visual(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='red', node_size=50)
    nx.draw_networkx_edges(G, pos, edge_color='yellow')
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='Arial')
    plt.axis('off')
    plt.show()
    return

def graph_calculation(G):
    cent_graph = nx.degree_centrality(G)
    i = 0
    cent = 0
    print('самый центральный узел/узлы:')
    for nodeid in sorted(cent_graph, key=cent_graph.get, reverse=True):
        if cent_graph[nodeid] < cent:
            break
        else:
            cent = cent_graph[nodeid]
            print(nodeid, round(cent_graph[nodeid], 3))
    print ('радиус графа')
    print(nx.radius(G))
    print(nx.average_clustering(G))
    return


def main(m, words):
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    G = graph_design(unpacking(m), words)
    graph_visual(G)
    graph_calculation(G)
    return

print("'утка_NOUN', 'гусь_NOUN', 'селезень_NOUN', 'птица_NOUN', 'страус_NOUN'")
main(m, words)
