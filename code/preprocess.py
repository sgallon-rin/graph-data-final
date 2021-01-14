#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/1/14 16:52
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : preprocess.py
# @Description :

import scipy.io as sio

DATA_DIR = "../data/"

data = sio.loadmat(DATA_DIR + "GD98_c.mat")
mat = data.get("Problem")["A"][0][0]
x = mat.nonzero()
print(x)