#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:35:08 2019

@author: Seahymn
"""
import pandas as pd
import numpy as np
import pickle
import os


def LoadSavedData(path):
    with open(path, 'rb') as f:
        loaded_data = pickle.load(f, encoding='utf-8')
    return loaded_data


# Get the csv file and convert it to a list.
def getData(filePath):
    df = pd.read_csv(filePath, sep=",", low_memory=False, header=None, encoding='latin1')
    df_list = df.values.tolist()

    # return df_list
    temp = []
    id_list = []
    ####
    for i in df_list:
        # Get rid of 'NaN' values.
        i = [x for x in i if str(x) != 'nan']
        if len(i) > 4:
            temp.append(i[1:])
            id_list.append(i[0])

    return temp, id_list


def GenerateLabels(input_arr):
    temp_arr = []
    for func_id in input_arr:
        temp_sub_arr = []
        if "cve" in func_id or "CVE" in func_id:
            temp_sub_arr.append(1)
        else:
            temp_sub_arr.append(0)
        temp_arr.append(temp_sub_arr)
    return np.asarray(temp_arr)


def SavedData(path, file_to_save):
    with open(path, 'wb') as handle:
        # pickle.dump(file_to_save, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(file_to_save, handle)


def dump_data_total(working_dir, directory):
    total_list = []
    total_list_id = []
    total_list_label = []
    directory_path = os.path.join(working_dir, directory)
    files_path = os.listdir(os.path.join(working_dir, directory))
    for file in files_path:
        list_pkl_file = os.path.join(directory_path, file, file + '_total_list.pkl')
        if os.path.isfile(list_pkl_file):
            total_list = total_list + LoadSavedData(list_pkl_file)
        id_pkl_file = os.path.join(directory_path, file, file + '_total_list_id.pkl')
        if os.path.isfile(id_pkl_file):
            total_list_id = total_list_id + LoadSavedData(id_pkl_file)
        label_pkl_file = os.path.join(directory_path, file, file + '_total_list_label.pkl')
        if os.path.isfile(label_pkl_file):
            total_list_label = total_list_label + LoadSavedData(label_pkl_file)
    return total_list, total_list_id, total_list_label


def dump_data_8_projects(working_dir, directory):
    total_list = []
    total_list_id = []
    total_list_label = []
    directory_path = os.path.join(working_dir, directory)
    Files_path = os.listdir(os.path.join(working_dir, directory))
    for file in Files_path:
        if file != 'Xen':
            list_pkl_file = os.path.join(directory_path, file, file + '_total_list.pkl')
            if os.path.isfile(list_pkl_file):
                total_list = total_list + LoadSavedData(list_pkl_file)
            id_pkl_file = os.path.join(directory_path, file, file + '_total_list_id.pkl')
            if os.path.isfile(id_pkl_file):
                total_list_id = total_list_id + LoadSavedData(id_pkl_file)
            label_pkl_file = os.path.join(directory_path, file, file + '_total_list_label.pkl')
            if os.path.isfile(label_pkl_file):
                total_list_label = total_list_label + LoadSavedData(label_pkl_file)
    return total_list, total_list_id, total_list_label


def dump_data_Xen(working_dir, directory):
    total_list = []
    total_list_id = []
    total_list_label = []
    directory_path = os.path.join(working_dir, directory)
    Files_path = os.listdir(os.path.join(working_dir, directory))
    for file in Files_path:
        if file == 'Xen':
            list_pkl_file = os.path.join(directory_path, file, file + '_total_list.pkl')
            if os.path.isfile(list_pkl_file):
                total_list = total_list + LoadSavedData(list_pkl_file)
            id_pkl_file = os.path.join(directory_path, file, file + '_total_list_id.pkl')
            if os.path.isfile(id_pkl_file):
                total_list_id = total_list_id + LoadSavedData(id_pkl_file)
            label_pkl_file = os.path.join(directory_path, file, file + '_total_list_label.pkl')
            if os.path.isfile(label_pkl_file):
                total_list_label = total_list_label + LoadSavedData(label_pkl_file)
    return total_list, total_list_id, total_list_label


def JoinSubLists(list_to_join):
    new_list = []

    for sub_list_token in list_to_join:
        new_line = ','.join(sub_list_token)
        new_list.append(new_line)
    return new_list


# Generate the directory which used to save model files,pkl file and loss curve graph
def Generate_saved_path(working_dir, model_name):
    saved_path = os.path.join(working_dir, model_name)
    model_saved_path = os.path.join(saved_path, 'models')
    model_saved_pkl_path = os.path.join(saved_path, 'pkl')
    model_saved_graph_path = os.path.join(saved_path, 'graph')
    if not os.path.exists(saved_path):
        os.mkdir(saved_path)
    if not os.path.exists(model_saved_path):
        os.mkdir(model_saved_path)
    if not os.path.exists(model_saved_pkl_path):
        os.mkdir(model_saved_pkl_path)
    if not os.path.exists(model_saved_graph_path):
        os.mkdir(model_saved_graph_path)


def Find_H5_file(dir, test_num):
    file_version = []
    file_lists = os.listdir(dir)
    epoch_old = 0
    for file in file_lists:
        num = file.count('_')
        file_split = file.split('_', num)
        file_version_str = file_split[0]
        #        max_epoch = file_split[5]
        if str(test_num) == file_version_str:
            file_version.append(file)
            epoch_new = int(file_split[-3])
            if epoch_new > epoch_old:
                epoch_old = epoch_new
    for file in file_version:
        num = file.count('_')
        if int(file.split('_', num)[-3]) == epoch_old:
            return file
