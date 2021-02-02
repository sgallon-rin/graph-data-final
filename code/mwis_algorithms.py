#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/1/30 13:33
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : mwis_algorithms.py
# @Description : 求解最大带权独立集MWIS的算法


import networkx as nx
from collections import defaultdict
from copy import deepcopy
from itertools import combinations
# from networkx.algorithms import approximation
from util.GraphLoader import GraphLoader
from util.util import WeightedIndependentSet


def exact_mwis(graph: nx.Graph) -> WeightedIndependentSet:
    """
    Exact MWIS Algorithm
    Recursive Function to find the Maximum Weighted Independent Vertex Set
    :param graph: nx.Graph
    :return: WeightedIndependentSet
    """
    # https://www.geeksforgeeks.org/maximal-independent-set-in-an-undirected-graph/
    S = WeightedIndependentSet()
    # Base Case - Given Graph has no nodes
    if len(graph.nodes) == 0:
        return S
    # Base Case - Given Graph has 1 node
    if len(graph.nodes) == 1:
        node = list(graph.nodes.data())[0]
        S.add_node(node[0], node[1]["weight"])  # node_name, node_weight
        return S
    # Select a vertex from the graph
    vCurrent = list(graph.nodes)[0]
    wCurrent = get_node_weight(vCurrent, graph)
    # Case 1 - Proceed removing the selected vertex from the Maximal Set
    graph1 = deepcopy(graph)
    # Delete current vertex from the Graph
    graph1.remove_node(vCurrent)
    # Recursive call - Gets Maximal Set, assuming current Vertex not selected
    res1 = exact_mwis(graph1)
    # Case 2 - Proceed considering the selected vertex as part of the Maximal Set
    # Loop through its neighbours
    for v in list(graph.adj[vCurrent]):
        # Delete neighbor from the current subgraph
        if v in graph1:
            graph1.remove_node(v)
    # This result set contains VFirst, and the result of recursive call assuming neighbors of vFirst are not selected
    res2 = exact_mwis(graph1)
    res2.add_node(vCurrent, wCurrent)
    # Our final result is the one which is bigger, return it
    if res1.get_weight() > res2.get_weight():
        return res1
    else:
        return res2


def single_reduction(graph: nx.Graph, if_sort=True) -> (WeightedIndependentSet, nx.Graph):
    """
    Single vertex reduction
    :param graph: nx.Graph
    :param if_sort: Bool
    :return: WIS got by reduction , graph after reduction
    """
    S = WeightedIndependentSet()
    T = []
    original_graph = deepcopy(graph)
    delta = defaultdict(int)
    if if_sort:
        node_list = sorted(dict(graph.nodes.data()).items(), key=lambda x: x[1]["weight"])
        node_list.reverse()
    else:
        node_list = dict(graph.nodes.data()).items()
    for node, d in node_list:
        if node not in graph.nodes:  # node has been removed in previous loops
            continue
        weight = d["weight"]
        for v in list(graph.adj[node]):
            delta[node] = delta[node] + get_node_weight(v, graph)
        if weight >= delta[node]:
            S.add_node(node, weight)
            for v in list(graph.adj[node]):
                graph.remove_node(v)
    while T:
        T_prime = T
        T = []
        for node in T_prime:
            if node not in graph.nodes:  # node has been removed in previous loops
                continue
            v_list = list(graph.adj[node])
            v_list.sort(key=lambda x: get_node_weight(x, original_graph), reverse=True)
            for v in v_list:
                if v not in graph.nodes:
                    continue
                delta[v] = delta[v] - get_node_weight(node, graph)
                if get_node_weight(v, graph) >= delta[v]:
                    S.add_node(v, get_node_weight(v, graph))
                    for w in list(graph.adj[v]):
                        graph.remove_node(w)
    return S, graph


def get_node_weight(node, graph: nx.Graph):
    return graph.nodes.data()[node]["weight"]


def calculate_nodes_weight(nodes, graph: nx.Graph):
    s = 0
    for node in nodes:
        if node in graph.nodes:
            s += get_node_weight(node, graph)
    return s


def two_reduction(graph: nx.Graph, if_sort=True) -> (WeightedIndependentSet, nx.Graph):
    """
    Two vertex reduction
    :param graph: nx.Graph
    :param if_sort: Bool
    :return: WIS got by reduction , graph after reduction
    """
    S = WeightedIndependentSet()
    used_dict = defaultdict(bool)
    if if_sort:
        node_list = sorted(dict(graph.nodes.data()).items(), key=lambda x: x[1]["weight"])
        node_list.reverse()
    else:
        node_list = dict(graph.nodes.data()).items()
    for node, d in node_list:
        if node not in graph.nodes:
            continue
        used_dict[node] = True
        weight_u = d["weight"]
        T = []
        for adj in list(graph.adj[node]):
            for adjadj in list(graph.adj[adj]):
                if used_dict[adjadj]:
                    continue
                if (node, adjadj) not in graph.edges:
                    T.append((adjadj, get_node_weight(adjadj, graph)))
        if if_sort:
            T.sort(key=lambda x: x[1], reverse=True)
        for v, weight_v in T:
            adj_u = list(graph.adj[node])
            adj_v = list(graph.adj[v])
            all_adj = set(adj_u + adj_v)
            if weight_u + weight_v >= calculate_nodes_weight(all_adj, graph):
                S.add_node(node, weight_u)
                S.add_node(v, weight_v)
                graph.remove_nodes_from(all_adj)
                graph.remove_node(node)
                graph.remove_node(v)
                break
    return S, graph


def k_reduction_exact(graph: nx.Graph, k=2, if_sort=True) -> (WeightedIndependentSet, nx.Graph):
    """
    k-vertex reduction exact
    :param graph: nx.Graph
    :param if_sort: Bool
    :return: WIS got by reduction , graph after reduction
    """
    S = WeightedIndependentSet()
    if if_sort:
        node_list = sorted(dict(graph.nodes.data()).items(), key=lambda x: x[1]["weight"])
        node_list.reverse()
    else:
        node_list = dict(graph.nodes.data()).items()
    for node, d in node_list:
        if node not in graph.nodes:
            continue
        weight_u = d["weight"]
        T = []
        for adj in list(graph.adj[node]):
            for adjadj in list(graph.adj[adj]):
                if (node, adjadj) not in graph.edges:
                    T.append(adjadj)
        ind_set_and_weight_in_T = calculate_independent_set(deepcopy(graph), T, k)  # [(nodes, weight), ...]
        if if_sort:
            ind_set_and_weight_in_T.sort(key=lambda x: x[1], reverse=True)
        for vs, weight_vs in ind_set_and_weight_in_T:
            adj_u = list(graph.adj[node])
            adj_vs = []
            for v in vs:
                adj_vs.extend(list(graph.adj[v]))
            all_adj = set(adj_u + adj_vs)
            if weight_u + weight_vs >= calculate_nodes_weight(all_adj, graph):
                S.add_node(node, weight_u)
                for v in vs:
                    S.add_node(v, get_node_weight(v, graph))
                graph.remove_nodes_from(all_adj)
                graph.remove_node(node)
                graph.remove_nodes_from(vs)
                break
    return S, graph


def calculate_independent_set(graph, T, k):
    """
    calculate independent set of size k
    :param graph: a nx.Graph
    :param T: several node tags in graph
    :param k: size of independent set to be calculated, k>1
    :return: all independent sets in graph with nodes from T of size k
    """
    if not T or k > len(T):
        return []
    assert k > 1, "k={} must be greater than one!".format(k)
    # assert k <= len(T), "k={} must be smaller than the size of T={}!".format(k, len(T))
    ind_set_list = []
    combinations_iter = combinations(T, k)
    for comb in combinations_iter:
        is_ind_set = True
        for pair in combinations(comb, r=2):
            if pair in graph.edges:
                is_ind_set = False
                break
        if is_ind_set:
            ind_set_list.append((comb, calculate_nodes_weight(comb, graph)))
    return ind_set_list


def check_independent_set(ind_set_dict, graph):
    nodes = list(ind_set_dict.keys())
    print("size of independent set is {}".format(len(nodes)))
    if len(nodes) <= 1:
        return True
    is_ind = True
    for pair in combinations(nodes, 2):
        if pair in graph.edges:
            is_ind = False
            break
    return is_ind


def main():
    original_graph =  GraphLoader.get_graph_from_graph("../graph-wo-self-loop/GD98_c.graph")
    # ====== 1 ======
    # g = GraphLoader.get_graph_from_graph("../graph-wo-self-loop/test.graph")
    # g = GraphLoader.get_graph_from_graph("../graph-wo-self-loop/GD98_c.graph")
    # weighted_ind_set = exact_mwis(g)
    # print(weighted_ind_set.get_weight())
    # ind_set = weighted_ind_set.get_independent_set()
    # print(ind_set)
    # ====== 2 ======
    # g = GraphLoader.get_graph_from_graph("../graph-wo-self-loop/GD98_c.graph")
    # # g = GraphLoader.get_graph_from_graph("../../graph-wo-self-loop/ca-AstroPh.graph")
    # weighted_ind_set, _ = single_reduction(g, if_sort=True)
    # print(weighted_ind_set.get_weight())
    # ind_set = weighted_ind_set.get_independent_set()
    # print(ind_set)
    # ====== 3 ======
    g = GraphLoader.get_graph_from_graph("../graph-wo-self-loop/GD98_c.graph")
    s1, g = single_reduction(g, if_sort=True)
    print(s1.get_weight())
    s2, _ = two_reduction(g, if_sort=True)
    s1.combine(s2)
    print(s1.get_weight())
    ind_set = s1.get_independent_set()
    print(ind_set)
    print(check_independent_set(ind_set, original_graph))
    # ====== 4 ======
    g = GraphLoader.get_graph_from_graph("../graph-wo-self-loop/GD98_c.graph")
    s1, g = single_reduction(g, if_sort=True)
    print(s1.get_weight())
    s2, g = two_reduction(g, if_sort=True)
    s1.combine(s2)
    print(s1.get_weight())
    s3, g = k_reduction_exact(g, k=3, if_sort=True)
    s1.combine(s3)
    print(s1.get_weight())
    s3, g = k_reduction_exact(g, k=4, if_sort=True)
    s1.combine(s3)
    print(s1.get_weight())
    s3, g = k_reduction_exact(g, k=5, if_sort=True)
    s1.combine(s3)
    print(s1.get_weight())
    ind_set = s1.get_independent_set()
    print(ind_set)
    print(check_independent_set(ind_set, original_graph))
    print("foo")


if __name__ == "__main__":
    main()
