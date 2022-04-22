# -*- coding: utf-8 -*-
"""
Created on Mon May 6 2019

@author: Seahymn
"""
import pickle
import csv
import os
import pandas as pd
from SRC.Configuration import Configuration


# Separate '(', ')', '{', '}', '*', '/', '+', '-', '=', ';', '[', ']' characters.

def SplitCharacters(str_to_split):
    # Character_sets = ['(', ')', '{', '}', '*', '/', '+', '-', '=', ';', ',']
    str_list_str = ''

    if '(' in str_to_split:
        str_to_split = str_to_split.replace('(',
                                            ' ( ')  # Add the space before and after the '(', so that it can be split by space.
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if ')' in str_to_split:
        str_to_split = str_to_split.replace(')',
                                            ' ) ')  # Add the space before and after the ')', so that it can be split by space.
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '{' in str_to_split:
        str_to_split = str_to_split.replace('{', ' { ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '}' in str_to_split:
        str_to_split = str_to_split.replace('}', ' } ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '*' in str_to_split:
        str_to_split = str_to_split.replace('*', ' * ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '/' in str_to_split:
        str_to_split = str_to_split.replace('/', ' / ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '+' in str_to_split:
        str_to_split = str_to_split.replace('+', ' + ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '-' in str_to_split:
        str_to_split = str_to_split.replace('-', ' - ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '=' in str_to_split:
        str_to_split = str_to_split.replace('=', ' = ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if ';' in str_to_split:
        str_to_split = str_to_split.replace(';', ' ; ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '[' in str_to_split:
        str_to_split = str_to_split.replace('[', ' [ ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if ']' in str_to_split:
        str_to_split = str_to_split.replace(']', ' ] ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '>' in str_to_split:
        str_to_split = str_to_split.replace('>', ' > ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '<' in str_to_split:
        str_to_split = str_to_split.replace('<', ' < ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '"' in str_to_split:
        str_to_split = str_to_split.replace('"', ' " ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '->' in str_to_split:
        str_to_split = str_to_split.replace('->', ' -> ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '>>' in str_to_split:
        str_to_split = str_to_split.replace('>>', ' >> ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if '<<' in str_to_split:
        str_to_split = str_to_split.replace('<<', ' << ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if ',' in str_to_split:
        str_to_split = str_to_split.replace(',', ' , ')
        str_list = str_to_split.split(' ')
        str_list_str = ' '.join(str_list)

    if str_list_str is not '':
        return str_list_str
    else:
        return str_to_split


def SavedData(path, file_to_save):
    with open(path, 'wb') as handle:
        pickle.dump(file_to_save, handle)


def Save3DList(save_path, list_to_save):
    with open(save_path, 'w', encoding='latin1') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerows(list_to_save)


def Save2DList(save_path, list_to_save):
    with open(save_path, 'w', encoding='latin1') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(list_to_save)


def ListToCSV(list_to_csv, path):
    df = pd.DataFrame(list_to_csv)
    df.to_csv(path, index=False)


def removeSemicolon(input_list):
    """
    Remove ';' from the list.
    :param input_list:
    :return:
    """
    new_list = []
    for line in input_list:
        new_line = []
        for item in line:
            if item != ';' and item != ',':
                new_line.append(item)
        new_list.append(new_line)

    return new_list


def ProcessList(list_to_process):
    """
    Further split the elements such as "const int *" into "const", "int" and "*"
    :param list_to_process:
    :return:
    """
    token_list = []
    for sub_list_to_process in list_to_process:
        sub_token_list = []
        if len(sub_list_to_process) != 0:
            for each_word in sub_list_to_process:  # Remove the empty row
                each_word = str(each_word)
                sub_word = each_word.split()
                for element in sub_word:
                    sub_token_list.append(element)
            token_list.append(sub_token_list)
    return token_list


def getCFilesFromText(path):
    files_list = []
    file_id_list = []
    for fpathe, dirs, fs in os.walk(path):
        for f in fs:
            if os.path.splitext(f)[1] == '.c':
                file_id_list.append(f)
            if os.path.splitext(f)[1] == '.c':
                with open(os.path.join(path, f), encoding='utf-8') as file:
                    lines = file.readlines()
                    file_list = []
                    for line in lines:
                        if line is not ' ' and line is not '\n':  # Remove sapce and line-change characters
                            sub_line = line.split()
                            new_sub_line = []
                            for element in sub_line:
                                new_element = SplitCharacters(element)
                                new_sub_line.append(new_element)
                            new_line = ' '.join(new_sub_line)
                            file_list.append(new_line)
                    new_file_list = ' '.join(file_list)
                    split_by_space = new_file_list.split()
                files_list.append(split_by_space)
        return files_list, file_id_list


def generate_pkl(path, directory):
    projects_path = os.path.abspath(os.path.join(path, directory))
    project_list = os.listdir(projects_path)

    for project in project_list:
        project_path = os.path.abspath(os.path.join(projects_path, project))

        non_vul_file_list, non_vul_file_list_id = getCFilesFromText(
            os.path.abspath(os.path.join(project_path, Configuration.Non_vul_func)))

        vul_file_list, vul_file_list_id = getCFilesFromText(
            os.path.abspath(os.path.join(project_path, Configuration.Vul_func)))

        new_non_vul_file_list = removeSemicolon(non_vul_file_list)
        new_vul_file_list = removeSemicolon(vul_file_list)

        non_vul_file_list_label = [0] * len(new_non_vul_file_list)
        vul_file_list_label = [1] * len(new_vul_file_list)

        total_list_all = new_non_vul_file_list + new_vul_file_list
        total_file_list_id = non_vul_file_list_id + vul_file_list_id
        total_file_list_label = non_vul_file_list_label + vul_file_list_label

        SavedData(os.path.join(project_path, project + '_non_vul_file_list.pkl'), new_non_vul_file_list)
        SavedData(os.path.join(project_path, project + '_non_vul_list_id.pkl'), non_vul_file_list_id)
        SavedData(os.path.join(project_path, project + '_non_vul_list_label.pkl'), non_vul_file_list_label)

        SavedData(os.path.join(project_path, project + '_vul_file_list.pkl'), new_vul_file_list)
        SavedData(os.path.join(project_path, project + '_vul_list_id.pkl'), vul_file_list_id)
        SavedData(os.path.join(project_path, project + '_vul_list_label.pkl'), vul_file_list_label)

        SavedData(os.path.join(project_path, project + '_total_list.pkl'), total_list_all)
        SavedData(os.path.join(project_path, project + '_total_list_id.pkl'), total_file_list_id)
        SavedData(os.path.join(project_path, project + '_total_list_label.pkl'), total_file_list_label)
