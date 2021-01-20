#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/1/15 14:03
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : util.py
# @Description : utilities


import os


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
