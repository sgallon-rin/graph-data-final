#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/1/14 16:52
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : preprocess.py
# @Description :


import random
import json
import numpy as np
import scipy.io as sio
import networkx as nx
import matplotlib.pyplot as plt
from util.util import listdir_remove_temp
from util.GraphLoader import GraphLoaderMat, GraphLoaderTxt, GraphLoaderJson


DATA_DIR = "../data/"
RANDOM_SEED = 123
RANDOM_WEIGHT_INTERVAL = (1, 200)


file_list = listdir_remove_temp(DATA_DIR)


def load_mat(filename):
    """
    load SSMC .mat file
    returns two list of nodes representing edges
    """
    data = sio.loadmat(filename)
    mat = data.get("Problem")["A"][0][0]
    x = mat.nonzero()
    from_node_list = x[0].tolist()
    to_node_list = x[1].tolist()
    return from_node_list, to_node_list


def make_weighted_graph_with_from_to_node_list(from_node_list, to_node_list, random_seed=RANDOM_SEED):
    """
    create a weighted undirected graph from two list of nodes representing edges
    randomly assign weight to each node if add_weight==True
    """
    assert len(from_node_list) == len(to_node_list), "from_node_list and to_node_list must have the same length!"
    random.seed(random_seed)
    G = nx.Graph()
    node_set = set(from_node_list).union(set(to_node_list))
    weighted_node_list = [(node, {"weight": random.randint(*RANDOM_WEIGHT_INTERVAL)}) for node in node_set]
    G.add_nodes_from(weighted_node_list)
    num_edges = len(from_node_list)
    for i in range(num_edges):
        G.add_edge(from_node_list[i], to_node_list[i])
    return G


def load_json(filename):
    """
    load .json file
    returns two list of nodes representing edges
    """
    pass


def draw_graph(G, pos=None):
    if not pos:
        pos = nx.spring_layout(G)
    nx.draw(G, pos)
    # plt.savefig("./G.png")
    plt.show()


#################### TEST ####################
def test_draw():
    G = nx.petersen_graph()
    # plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    # plt.subplot(122)
    nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    plt.show()
#################### END TEST ####################

def main():
    print("foo")


if __name__ == "__main__":
    fnode_list, tnode_list = load_mat(DATA_DIR + "GD98_c.mat")
    G = make_weighted_graph_with_from_to_node_list(fnode_list, tnode_list)
    pos = nx.spring_layout(G)
    draw_graph(G, pos)
    # draw_graph(G, pos)
    np.save("G.graph", G)
    # test_draw()
    main()
