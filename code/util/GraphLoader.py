#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/1/15 14:03
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : GraphLoader.py
# @Description : classes for loading and generating weighted graph from original dataset


import abc
import joblib
import json
import os.path
import random
import networkx as nx
import scipy.io as sio


class GraphLoader(metaclass=abc.ABCMeta):
    """abstract class for load data and generate weighted graph"""
    _cls_filetype = "graph"

    def __init__(self):
        self._filetype = None
        self.graph = None
        self.data = None

    @classmethod
    def _check_file_type_cls(cls, file: str):
        in_filetype = file.split(".")[-1]
        if in_filetype != cls._cls_filetype:
            raise TypeError("Expect file type {}, but got {}. \nCurrent filename is {}"
                            .format(cls._cls_filetype, in_filetype, os.path.abspath(file)))

    @classmethod
    def get_graph_from_graph(cls, file: str) -> nx.Graph:
        """
        read graph from saved .graph file and return it
        class method, does not save the graph into object
        """
        cls._check_file_type_cls(file)
        graph = joblib.load(file)
        print("Successfully loaded graph from {}".format(os.path.abspath(file)))
        cls.print_graph_info(graph)
        return graph

    @classmethod
    def print_graph_info(cls, graph):
        print("#######\nGraph info:\nNodes: {}\nEdges: {}\n######".format(len(graph.nodes), len(graph.edges)))

    def _check_file_type(self, file: str):
        in_filetype = file.split(".")[-1]
        if in_filetype != self._filetype:
            raise TypeError("Expect file type {}, but got {}. \nCurrent filename is {}"
                            .format(self._filetype, in_filetype, os.path.abspath(file)))

    def load_graph_from_graph(self, file: str):
        """load graph from .graph file"""
        self._check_file_type_cls(file)
        self.graph = joblib.load(file)
        print("Successfully loaded graph from {}".format(os.path.abspath(file)))
        self.print_graph_info(self.graph)

    def load_graph_from_raw(self, file: str, random_seed: int, weight_interval):
        self._check_file_type(file)
        self._load_raw_data(file)
        print("Successfully loaded raw data from file {}".format(os.path.abspath(file)))
        self._make_graph(random_seed, weight_interval)
        print("Successfully generated graph!")
        self.print_graph_info(self.graph)

    def save_graph(self, file: str):
        """save graph to file"""
        joblib.dump(self.graph, file)
        print("Successfully saved graph to {}".format(os.path.abspath(file)))

    @abc.abstractmethod
    def _load_raw_data(self, file: str):
        raise NotImplementedError

    @abc.abstractmethod
    def _make_graph(self, random_seed: int, weight_interval):
        raise NotImplementedError


class GraphLoaderMat(GraphLoader):
    """class for load data and generate weighted graph from SSMC format .mat file"""
    def __init__(self):
        super().__init__()
        self._filetype = "mat"

    def _load_raw_data(self, file):
        """
        load SSMC .mat file
        returns two lists of nodes representing edges
        """
        data = sio.loadmat(file)
        mat = data.get("Problem")["A"][0][0]
        x = mat.nonzero()
        from_node_list = x[0].tolist()
        to_node_list = x[1].tolist()
        if len(from_node_list) != len(to_node_list):
            raise ValueError("from_node_list and to_node_list must have the same length!")
        self.data = (from_node_list, to_node_list)

    def _make_graph(self, random_seed, weight_interval):
        """
        create a weighted undirected graph from two list of nodes representing edges
        randomly assign weight to each node
        """
        from_node_list, to_node_list = self.data
        random.seed(random_seed)
        node_set = set(from_node_list).union(set(to_node_list))
        weighted_node_list = [(node, {"weight": random.randint(*weight_interval)}) for node in node_set]
        g = nx.Graph()
        g.add_nodes_from(weighted_node_list)
        num_edges = len(from_node_list)
        for i in range(num_edges):
            g.add_edge(from_node_list[i], to_node_list[i])
        self.graph = g


class GraphLoaderTxt(GraphLoader):
    """class for load data and generate weighted graph from SNAP format .txt file"""
    def __init__(self):
        super().__init__()
        self._filetype = "txt"

    def _load_raw_data(self, file: str):
        node_set = set()
        edge_list = []
        with open(file, 'r', encoding='utf-8') as handler:
            for line in handler:
                if line.strip().startswith("#"):
                    continue
                # use int instead of string as node name to reduce saved size
                node_i, node_j = map(int, line.strip().split())
                node_set.add(node_i)
                node_set.add(node_j)
                edge_list.append((node_i, node_j))
        self.data = (node_set, edge_list)

    def _make_graph(self, random_seed, weight_interval):
        node_set, edge_list = self.data
        random.seed(random_seed)
        weighted_node_list = [(node, {"weight": random.randint(*weight_interval)}) for node in node_set]
        g = nx.Graph()
        g.add_nodes_from(weighted_node_list)
        g.add_edges_from(edge_list)
        self.graph = g


class GraphLoaderJson(GraphLoader):
    """
    class for load data and generate weighted graph from .json file
    original data description: https://github.com/evelinag/StarWars-social-network/tree/master/networks
    """
    def __init__(self):
        super().__init__()
        self._filetype = "json"

    def _load_raw_data(self, file: str):
        with open(file, 'r', encoding='utf-8') as handler:
            json_record = json.loads(handler.read())
        node_dict_list = json_record['nodes']
        edge_dict_list = json_record['links']
        node_list = [(node_dict['name'], {"weight": node_dict['value'], "colour": node_dict["colour"]})
                     for node_dict in node_dict_list]
        index_edge_list = [(edge_dict['source'], edge_dict['target']) for edge_dict in edge_dict_list]  # [(1, 2), ...]
        node_name_list = [t[0] for t in node_list]
        named_edge_list = []  # [("Foo", "Bar"), ...]
        for edge in index_edge_list:
            node_i_name = node_name_list[edge[0]]
            node_j_name = node_name_list[edge[1]]
            named_edge_list.append((node_i_name, node_j_name))
        self.data = (node_list, named_edge_list)

    def _make_graph(self, random_seed=None, weight_interval=None):
        node_list, edge_list = self.data
        g = nx.Graph()
        g.add_nodes_from(node_list)
        g.add_edges_from(edge_list)
        self.graph = g


if __name__ == "__main__":
    # fname = "../../data/GD98_c.mat"
    # gname = "../../graph/GD98_c.graph"
    # graphloader = GraphLoaderMat()
    # graphloader.load_raw_data(fname)
    # graphloader.make_graph(123, (1, 200))
    # G = graphloader.get_graph()
    fname = "../../data/ca-AstroPh.txt"
    gname = "../../graph/ca-AstroPh.graph"
    graphloader = GraphLoaderTxt()
    # fname = "../../data/starwars-full-interactions.json"
    # gname = "../../graph/starwars-full-interactions.graph"
    # graphloader = GraphLoaderJson()
    graphloader.load_graph_from_raw(fname, 123, (1, 200))
    G = graphloader.graph
    graphloader.save_graph(gname)
    GG = GraphLoader.get_graph_from_graph(gname)
    print("foo")
