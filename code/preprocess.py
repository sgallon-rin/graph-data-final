#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/1/14 16:52
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : preprocess.py
# @Description : load data from raw file, change them into (node-weighted & undirected) graph and save them


from util.util import listdir_remove_temp
from util.GraphLoader import GraphLoaderMat, GraphLoaderTxt, GraphLoaderJson


DATA_DIR = "../data/"
GRAPH_DIR = "../graph/"
RANDOM_SEED = 123
RANDOM_WEIGHT_INTERVAL = (1, 200)
FILETYPE_DICT = {"mat": GraphLoaderMat, 'json': GraphLoaderJson, 'txt': GraphLoaderTxt}
# FILETYPE_DICT = {"mat": GraphLoaderMat, 'json': GraphLoaderJson}

def load_raw_and_save_graph(loadfile: str, savefile: str):
    filename, filetype = loadfile.split('/')[-1].split('.')
    if filetype not in FILETYPE_DICT.keys():
        # raise TypeError("Filetype {} incorrect! Must be in {}".format(filetype, FILETYPE_DICT.keys()))
        print("Filetype {} incorrect! Must be in {}".format(filetype, FILETYPE_DICT.keys()))
        return
    graphloader = FILETYPE_DICT[filetype]()
    graphloader.load_graph_from_raw(loadfile, random_seed=RANDOM_SEED, weight_interval=RANDOM_WEIGHT_INTERVAL)
    graphloader.save_graph(savefile)


def main():
    file_list = listdir_remove_temp(DATA_DIR)
    for idx, file in enumerate(file_list):
        print("------ <{:^3d}> ------".format(idx))
        load_raw_and_save_graph(DATA_DIR + file, GRAPH_DIR + file.split('.')[0] + ".graph")


if __name__ == "__main__":
    main()
