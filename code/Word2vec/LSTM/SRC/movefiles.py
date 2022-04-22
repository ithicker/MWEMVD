#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 12:20:02 2019

@author: Seahymn
"""

import os
import random
import shutil
from SRC.Configuration import Configuration


def traversal_dir_for_first_level_dir(path) -> "folder name list":
    """
    遍历传入路径下的文件，将第一层文件夹名放入list
    path:传入的目标路径
    """
    folder_list = []
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path, file)
            if os.path.isdir(m):
                h = os.path.split(m)  # 将文件夹路径切分成路径和文件夹名
                folder_list.append(h[1])  # 保存文件夹名到列表正
    return folder_list


def generate_dir(data_path, FirstDir, folder1, folder2) -> "创建的文件夹路径":
    testDir = []
    for i in range(len(FirstDir)):

        tempDir = os.path.abspath(os.path.join(data_path, folder1))
        if not os.path.exists(tempDir):
            os.mkdir(tempDir)
        tempDir = os.path.abspath(os.path.join(tempDir, str(FirstDir[i])))
        if not os.path.exists(tempDir):
            os.mkdir(tempDir)
        tempDir = os.path.abspath(os.path.join(tempDir, folder2))
        if not os.path.exists(tempDir):
            os.mkdir(tempDir)
        testDir.append(tempDir)
    print(testDir)
    return testDir


def move_files(pathDir, testDir, trainDir, validationDir, testPercent=0.2, trainPercent=0.6):
    datafiles = os.listdir(pathDir)
    data_num = len(datafiles)
    index_list = list(range(data_num))
    random.shuffle(index_list)
    for i in index_list:
        file_name = os.path.join(pathDir, datafiles[i])
        if os.path.splitext(datafiles[i])[1] == '.c':
            if i < data_num * testPercent:
                shutil.move(file_name, testDir)
            else:
                if i < data_num * (1 - trainPercent):
                    shutil.move(file_name, validationDir)
                else:
                    shutil.move(file_name, trainDir)  # Move files from dir1 to dir2


def make_dir_and_move_files() -> "数据存放路径列表":
    FirstDir = traversal_dir_for_first_level_dir(Configuration.Func_path)
    data_folder_list = []

    Non_vul_func_trainDir = generate_dir(Configuration.data_path, FirstDir, 'Train', Configuration.Non_vul_func)  # 生成不易感染样本训练目录
    data_folder_list.append(Non_vul_func_trainDir)
    Non_vul_func_testDir = generate_dir(Configuration.data_path, FirstDir, 'Test', Configuration.Non_vul_func)  # 生成不易感染样本测试目录
    data_folder_list.append(Non_vul_func_testDir)
    Non_vul_func_validationDir = generate_dir(Configuration.data_path, FirstDir, 'Validation', Configuration.Non_vul_func)  # 生成不易感染样本验证目录
    data_folder_list.append(Non_vul_func_validationDir)
    Vul_func_trainDir = generate_dir(Configuration.data_path, FirstDir, 'Train', Configuration.Vul_func)  # 生成易感染样本训练目录
    data_folder_list.append(Vul_func_trainDir)
    Vul_func_testDir = generate_dir(Configuration.data_path, FirstDir, 'Test', Configuration.Vul_func)  # 生成易感染样本测试目录
    data_folder_list.append(Vul_func_testDir)
    Vul_func_validationDir = generate_dir(Configuration.data_path, FirstDir, 'Validation', Configuration.Vul_func)  # 生成易感染样本验证目录
    data_folder_list.append(Vul_func_validationDir)

    for i in range(len(FirstDir)):
        pathDir = os.path.join(Configuration.Func_path, str(FirstDir[i]), Configuration.Non_vul_func)
        move_files(pathDir, Non_vul_func_testDir[i], Non_vul_func_trainDir[i], Non_vul_func_validationDir[i])
        pathDir = os.path.join(Configuration.Func_path, str(FirstDir[i]), Configuration.Vul_func)
        move_files(pathDir, Vul_func_testDir[i], Vul_func_trainDir[i], Vul_func_validationDir[i])

    return data_folder_list
