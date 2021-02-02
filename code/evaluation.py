#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/2/2 11:51
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : evaluation.py
# @Description : Runs mwis and evaluate them.
# @Usage       : $ python ./code/evaluation.py ./graph/ca-GrQc.graph True


import time
import sys
import networkx as nx
from copy import deepcopy
from util.GraphLoader import GraphLoader
from mwis_algorithms import single_reduction, two_reduction, k_reduction_exact


def alg1(graph: nx.Graph):
    """DtSingle - single vertex reduction without sort"""
    start_time = time.time()
    s1, _ = single_reduction(graph, if_sort=False)
    print("alg1 done!")
    return s1.get_size(), s1.get_weight(), time.time() - start_time


def alg2(graph: nx.Graph):
    """DtSingleS - single vertex reduction with sort"""
    start_time = time.time()
    s1, _ = single_reduction(graph, if_sort=True)
    print("alg2 done!")
    return s1.get_size(), s1.get_weight(), time.time() - start_time


def alg3(graph: nx.Graph):
    """DtTwo - single + two vertex reduction without sort"""
    start_time = time.time()
    s1, g = single_reduction(graph, if_sort=False)
    s2, _ = two_reduction(g, if_sort=False)
    s1.combine(s2)
    print("alg3 done!")
    return s1.get_size(), s1.get_weight(), time.time() - start_time


def alg4(graph: nx.Graph):
    """DtTwoS - single + two vertex reduction with sort"""
    start_time = time.time()
    s1, g = single_reduction(graph, if_sort=True)
    s2, _ = two_reduction(g, if_sort=True)
    s1.combine(s2)
    print("alg4 done!")
    return s1.get_size(), s1.get_weight(), time.time() - start_time


def alg5_6_7(graph: nx.Graph):
    """EDtk - single + two + k vertex reduction with sort"""
    start_time = time.time()
    s1, g = single_reduction(graph, if_sort=True)
    s2, g = two_reduction(g, if_sort=True)
    s1.combine(s2)
    s3, g = k_reduction_exact(g, k=3, if_sort=True)
    s1.combine(s3)
    size_alg5 = s1.get_size()
    weight_alg5 = s1.get_weight()
    t_alg5 = time.time() - start_time
    print("alg5 done!")
    s4, g = k_reduction_exact(g, k=4, if_sort=True)
    s1.combine(s4)
    size_alg6 = s1.get_size()
    weight_alg6 = s1.get_weight()
    t_alg6 = time.time() - start_time
    print("alg6 done!")
    s5, g = k_reduction_exact(g, k=5, if_sort=True)
    s1.combine(s5)
    size_alg7 = s1.get_size()
    weight_alg7 = s1.get_weight()
    t_alg7 = time.time() - start_time
    print("alg7 done!")
    return (size_alg5, weight_alg5, t_alg5), (size_alg6, weight_alg6, t_alg6), (size_alg7, weight_alg7, t_alg7)


def evaluate(filename, skip34=False, skip567=False):
    if skip34:
        skip567 = True
    size_list = []
    weight_list = []
    graph = GraphLoader.get_graph_from_graph(filename)
    res1 = alg1(deepcopy(graph))
    size_list.append(res1[0])
    weight_list.append(res1[1])
    res2 = alg2(deepcopy(graph))
    size_list.append(res2[0])
    weight_list.append(res2[1])
    if not skip34:
        res3 = alg3(deepcopy(graph))
        size_list.append(res3[0])
        weight_list.append(res3[1])
        res4 = alg4(deepcopy(graph))
        size_list.append(res4[0])
        weight_list.append(res4[1])
    if not skip567:
        res5, res6, res7 = alg5_6_7(deepcopy(graph))
        size_list.append(res5[0])
        weight_list.append(res5[1])
        size_list.append(res6[0])
        weight_list.append(res6[1])
        size_list.append(res7[0])
        weight_list.append(res7[1])
    rp = relative_precision(weight_list)
    # ====== print ======
    print("algorithm\tsize\tweight\ttime\trp")
    print("DtSingle\t{}\t{}\t{}\t{}".format(*res1, rp[0]))
    print("DtSingleS\t{}\t{}\t{}\t{}".format(*res2, rp[1]))
    if not skip34:
        print("DtTwo\t{}\t{}\t{}\t{}".format(*res3, rp[2]))
        print("DtTwoS\t{}\t{}\t{}\t{}".format(*res4, rp[3]))
    if not skip567:
        print("EDtk(k=3)\t{}\t{}\t{}\t{}".format(*res5, rp[4]))
        print("EDtk(k=4)\t{}\t{}\t{}\t{}".format(*res6, rp[5]))
        print("EDtk(k=5)\t{}\t{}\t{}\t{}".format(*res7, rp[6]))


def relative_precision(weight_list):
    max_w = max(weight_list)
    return [w/max_w for w in weight_list]


def str2bool(s):
    if s in ["True", "TRUE", "true"]:
        return True
    else:
        return False


if __name__ == "__main__":
    filename = sys.argv[1]
    if len(sys.argv) > 2:
        skip34 = str2bool(sys.argv[2])
        skip567 = str2bool(sys.argv[3])
        evaluate(filename, skip34, skip567)
    else:
        evaluate(filename)
