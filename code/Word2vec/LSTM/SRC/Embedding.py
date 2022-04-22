# -*- coding: utf-8 -*-
"""
Created on Tue May 7 2019

@author: Seahymn
"""

import os
import pickle
# from gensim.models import Word2Vec
from keras.preprocessing.text import Tokenizer
from SRC.Configuration import Configuration
#insert zero
import re
from mittens import GloVe
import numpy as np
import jieba
from gensim import corpora
#######################################
def LoadData(file_to_load):
    """
    Load the *.pkl data.
    :param file_to_load: pickle file to be loaded
    :return: pickle file content
    """
    with open(file_to_load, 'rb') as f:
        loaded_file = pickle.load(f)
    return loaded_file


def total(working_dir, directory):
    tmp_total_list = []
    projects_path = os.path.abspath(os.path.join(working_dir, directory))
    project_list = os.listdir(projects_path)
    for project in project_list:
        path = os.path.join(projects_path, project)
        pkl_file = os.path.join(path, project + '_total_list.pkl')
        if os.path.isfile(pkl_file):
            func_list = LoadData(pkl_file)
            tmp_total_list = tmp_total_list + func_list
    return tmp_total_list

#insert—one
def Bottom_Top(c_pos, max_len, window):
    bottom = c_pos - window
    top = c_pos + window + 1
    if bottom < 0:
        bottom = 0
    if top >= max_len:
        top = max_len
    return bottom, top

##############################
def do_embed():
    total_list = total(Configuration.data_path, 'Train') + \
                 total(Configuration.data_path, 'Validation') + \
                 total(Configuration.data_path, 'Test')
    print("The length of the list is : " + str(len(total_list)))

    # --------------------------------------------------------#
    # 2. Tokenization: convert the loaded text (the nodes of ASTs) to tokens.

    new_total_token_list = []

    for sub_list_token in total_list:
        new_line = ','.join(sub_list_token)
        new_total_token_list.append(new_line)
    ####################
    # 生成词汇相关矩阵
    dict = corpora.Dictionary(total_list)
    token_id = dict.token2id
    # 生成词汇相关矩阵
    n_matrix = len(token_id)
    window = 5
    word_matrix = np.zeros(shape=[n_matrix, n_matrix])
    n_dims = 100
    #insert two
    for i in range(len(total_list)):
        k = len(total_list[i])
        for j in range(k):
            bottom, top = Bottom_Top(j, k, window)
            c_word = total_list[i][j]
            c_pos = token_id[c_word]
            for m in range(bottom, top):
                # 计算矩阵
                t_word = total_list[i][m]
                if m != j and t_word != c_word:
                    t_pos = token_id[t_word]
                    word_matrix[c_pos][t_pos] += 1
    ############################
    tokenizer = Tokenizer(num_words=None, filters=',', lower=False, char_level=False, oov_token=None)
    tokenizer.fit_on_texts(new_total_token_list)

    # Save the tokenizer.
    with open(os.path.abspath(os.path.join(Configuration.data_path, 'all_matrix_no_comments.pickle')), 'wb') as handle:
        pickle.dump(tokenizer, handle)
    #
    # # ----------------------------------------------------- #
    # # 3. Train a Vocabulary with Word2Vec -- using the function provided by gensim
    #
    # # w2v_model = Word2Vec(train_token_list, workers = 12, size=100)
    # # With default settings, the embedding dimension is 100 and using, (sg=0), CBOW is used.
    # w2v_model = Word2Vec(total_list, workers=12)
    #
    # print("----------------------------------------")
    # print("The trained word2vec model: ")
    # print(w2v_model)
    #
    # w2v_model.wv.save_word2vec_format(
    #     os.path.abspath(os.path.join(Configuration.data_path, 'all_w2v_model_CBOW_no_comments.txt')), binary=False)

    #insert three
    # 用Mittens计算
    glove = GloVe(n=n_dims, max_iter=10, learning_rate=0.005)
    G = glove.fit(word_matrix)
    # G_numpy = G.numpy()
    items_index = []
    for keys, items in dict.iteritems():
        items_index.append(items)
    out_str = []
    for i in range(len(token_id)):
        s = items_index[i]
        for j in range(n_dims):
            s = s + " " + str(G[i][j])
        out_str.append(s)
    # Vector写入文件中
    f = open(os.path.abspath(os.path.join(Configuration.data_path, 'mittens.txt')), 'w+', encoding="utf-8")
    s = str(len(token_id)) + " " + str(n_dims) + "\n"
    f.write(s)
    for i in out_str:
        f.write(i)
        f.write("\n")
    f.close()
    ####################################################
