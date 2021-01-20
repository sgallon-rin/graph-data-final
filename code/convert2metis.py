#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/1/20 10:02
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : convert2metis.py
# @Description : 数据格式转换，以便使用KaMIS(https://karlsruhemis.github.io)
# 有关数据格式请参照文档 http://algo2.iti.kit.edu/schulz/software_releases/kamis.pdf
# 请在code文件夹下执行
# @Usage       :  $ python convert2metis.py <graph文件名>


import sys
import os.path
from tqdm import tqdm
from util.util import listdir_remove_temp
from util.GraphLoader import GraphLoader


GRAPH_DIR = "../graph/"
METIS_DIR = "../metis/"


def load_convert_graph_save_metis(loadfile: str, savefile: str):
    """
    load a .graph graph, convert a networkx graph to a txt file to the format metis, as required br KaMIS
    :param loadfile: string, filepath to load
    :param savefile: string, filepath to save
    :return:
    """
    graph = GraphLoader.get_graph_from_graph(loadfile)
    num_nodes = len(graph.nodes)
    num_edges = len(graph.edges)
    node_list = list(graph.nodes)
    node_count = 0
    adj_dict = dict(graph.adjacency())
    with open(savefile, 'w') as handler:
        handler.write("{} {} 10\n".format(num_nodes, num_edges))  # 10 denotes node weighted
        for node in tqdm(node_list, ncols=80):
            node_count += 1
            weight = graph.nodes.data()[node]["weight"]
            adj = sorted([node_list.index(v)+1 for v in adj_dict[node].keys()])
            adj = " ".join([str(v) for v in adj])
            handler.write("{} {}\n".format(weight, adj))
    print("Count node: {}\nis equal to original: {}".format(node_count, node_count==num_nodes))
    print("Conversion done! Converted metis graph saved to {}".format(os.path.abspath(savefile)))


def main():
    file_list = listdir_remove_temp(GRAPH_DIR)
    for idx, file in enumerate(file_list):
        print("------ <{:^3d}> ------".format(idx))
        load_convert_graph_save_metis(GRAPH_DIR + file, METIS_DIR + file.split('.')[0] + ".metis.txt")


if __name__ == "__main__":
    # main()
    f = sys.argv[1]
    # f = "GD98_c.graph"
    load_convert_graph_save_metis(GRAPH_DIR + f, METIS_DIR + f.split('.')[0] + ".metis.txt")
