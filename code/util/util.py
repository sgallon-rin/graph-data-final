#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/1/15 14:03
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : util.py
# @Description : utilities


import os
import networkx as nx


def listdir_remove_temp(directory):
    """
    获取文件列表并移除macOS系统临时文件
    :param directory: string
    :return: list(string)
    """
    file_list = os.listdir(directory)
    if ".DS_Store" in file_list:
        file_list.remove(".DS_Store")
    return file_list


class WeightedIndependentSet:
    def __init__(self):
        self.nodes = dict()
        self.weight = 0

    def get_weight(self):
        self.weight = sum(self.nodes.values())
        return self.weight

    def get_size(self):
        return len(self.nodes)

    def add_node(self, node_name, node_weight):
        self.nodes[node_name] = node_weight

    def add_nodes(self, node_name_weight_list):
        for node_name, node_weight in node_name_weight_list:
            self.add_node(node_name, node_weight)

    def combine(self, wis):
        self.nodes.update(wis.nodes)

    def remove(self, node_name):
        _ = self.nodes.pop(node_name)

    def get_independent_set(self):
        return self.nodes
