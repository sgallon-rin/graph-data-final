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
    def __init__(self):
        self._filetype = None
        self.graph = None
        self.data = None

    @classmethod
    def load_get_graph(cls, file) -> nx.Graph:
        """load graph from file and return it"""
        print("Successfully loaded graph from {}".format(os.path.abspath(file)))
        return joblib.load(file)

    def get_graph(self) -> nx.Graph:
        """returns a networkx.Graph G"""
        return self.graph

    def load_graph(self, file):
        """load graph from file"""
        self.graph = joblib.load(file)
        print("Successfully loaded graph from {}".format(os.path.abspath(file)))

    def save_graph(self, file):
        """save graph to file"""
        joblib.dump(self.graph, file)
        print("Successfully saved graph to {}".format(os.path.abspath(file)))

    @abc.abstractmethod
    def load_data(self, file: str):
        raise NotImplementedError

    @abc.abstractmethod
    def make_graph(self, random_seed, weight_interval):
        raise NotImplementedError


# TODO: GraphLoader
class GraphLoaderMat(GraphLoader):
    """class for load data and generate weighted graph from SSMC format .mat file"""
    def __init__(self):
        super().__init__()
        self._filetype = "mat"

    def load_data(self, file):
        """
        load SSMC .mat file
        returns two lists of nodes representing edges
        """
        in_filetype = file.split(".")[-1]
        if in_filetype != self._filetype:
            raise TypeError("Expect file type {}, but got {}.".format(self._filetype, in_filetype))
        data = sio.loadmat(file)
        mat = data.get("Problem")["A"][0][0]
        x = mat.nonzero()
        from_node_list = x[0].tolist()
        to_node_list = x[1].tolist()
        if len(from_node_list) != len(to_node_list):
            raise ValueError("from_node_list and to_node_list must have the same length!")
        self.data = (from_node_list, to_node_list)
        print("Successfully loaded data from file {}".format(os.path.abspath(file)))

    def make_graph(self, random_seed, weight_interval):
        """
        create a weighted undirected graph from two list of nodes representing edges
        randomly assign weight to each node
        """
        from_node_list, to_node_list = self.data
        random.seed(random_seed)
        g = nx.Graph()
        node_set = set(from_node_list).union(set(to_node_list))
        weighted_node_list = [(node, {"weight": random.randint(*weight_interval)}) for node in node_set]
        g.add_nodes_from(weighted_node_list)
        num_edges = len(from_node_list)
        for i in range(num_edges):
            g.add_edge(from_node_list[i], to_node_list[i])
        self.graph = g
        print("Successfully generated graph!")


class GraphLoaderTxt(GraphLoader):
    """class for load data and generate weighted graph from SNAP format .txt file"""
    def __init__(self):
        super().__init__()
        self._filetype = "txt"

    def load_data(self, file: str):

        self.data = 1
        pass

    def make_graph(self, random_seed, weight_interval):
        pass


class GraphLoaderJson(GraphLoader):
    """class for load data and generate weighted graph from .json file"""
    def __init__(self):
        super().__init__()
        self._filetype = "json"

    def load_data(self, file: str):
        self.data = 1
        pass

    def make_graph(self, random_seed, weight_interval):
        pass


if __name__ == "__main__":
    fname = "../../data/GD98_c.mat"
    gname = "../../graph/GD98_c.graph"
    glm = GraphLoaderMat()
    glm.load_data(fname)
    glm.make_graph(123, (1, 200))
    G = glm.get_graph()
    glm.save_graph(gname)
    GG = GraphLoader.load_get_graph(gname)
    print("foo")
