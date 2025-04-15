import json
import numpy as np
from itertools import chain
import networkx as nx
from networkx.algorithms import bipartite


def dict2json(d, write_file):
    j = json.dumps(d, indent = 4)
    with open(write_file,'w') as w_f:
        w_f.write(j)

def json2dict(read_file):
    with open(read_file, "r") as json_file:
        data = json.load(json_file)
    return data

def dict2countdict(d, keys):
    countdict = {key: 0 for key in keys}
    for key in d.keys():
        countdict.update({key: len(d[key])})
    return countdict

def reverse_dict(d):
    new_d = {}
    for k, v in d.items():
        for i in v:
            new_d.setdefault(i, []).append(k)
    return new_d

def Bipartite_graph(dict_data, set_name):
    Bi_graph = nx.Graph()
    top_set = dict_data.keys() 
    bot_set = set(list(chain.from_iterable(dict_data.values())))  
    print('Total ' + set_name[0] + '(top): ', len(top_set))
    print('Total ' + set_name[1] + '(bot): ', len(bot_set))
    Bi_graph.add_nodes_from(top_set,bipartite = 0) # set 0: spice recipes
    Bi_graph.add_nodes_from(bot_set,bipartite = 1) # set 1: spices
    for key in top_set:
        for v in dict_data[key]:
            Bi_graph.add_edges_from([(key,v)])
    return Bi_graph, top_set, bot_set

def extract_backbone(g, alpha):
    backbone_graph = nx.Graph()
    for node in g:
        k_n = len(g[node]) # k_n: number of neighbors of given node in g
        if(k_n > 1):
            sum_w = sum( g[node][neighbor]['weight'] for neighbor in g[node] ) #sum of edge weights from given node
            for neighbor in g[node]:
                edgeWeight = g[node][neighbor]['weight']
                pij = float(edgeWeight)/sum_w    # pij = single edgeweight/ total edge weights
                if (1-pij)**(k_n-1) < alpha: # equation 2 , single edgeweight higher, value smaller < alpha, then keep edge
                    backbone_graph.add_edge( node,neighbor, weight = edgeWeight)
    return backbone_graph

def Projection_graph(Bi_graph, mode):
    top_nodes = {n for n, d in Bi_graph.nodes(data=True) if d['bipartite']==0}
    bottom_nodes = set(Bi_graph) - top_nodes
    print('# nodes in Bi_graph: ', Bi_graph.number_of_nodes())
    top_projection = bipartite.weighted_projected_graph(Bi_graph, top_nodes) 
    bot_projection = bipartite.weighted_projected_graph(Bi_graph, bottom_nodes) 
    if (mode == 'top'): return top_projection
    if (mode == 'bot'): return bot_projection
    
def Adjmtx_to_Nodexl(g,file):
    # GENERATE ADJACENCY MTX AND STORE IN EXCEL
    G_adj_mtx = nx.to_pandas_adjacency(g)
    writer = ExcelWriter(file)
    G_adj_mtx.to_excel(writer,'Sheet1')
    writer.save()

