#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:03:32 2019

@author: Seahymn
"""
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "2"
import datetime
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.callbacks import TensorBoard, CSVLogger
from SRC.Functions import dump_data_total, dump_data_8_projects, LoadSavedData, JoinSubLists, SavedData, \
    Generate_saved_path
from SRC.LSTM_model_CPU import LSTM_network
from SRC.Configuration import Configuration

# --------------------------------------------------------------------------------------------------
# Parameters used
# --------------------------------------------------------------------------------------------------

MAX_LEN = 1000  # The Padding Length for each sample.
EMBEDDING_DIM = 100  # The Embedding Dimension for each element within the sequence of a data sample.
LOSS_FUNCTION = 'binary_crossentropy'
# OPTIMIZER = 'adamax'
OPTIMIZER = 'sgd'
BATCH_SIZE = 16
EPOCHS = 100
PATIENCE = 35

model_name = 'LSTM_8_Projects'

Start = 0
LoopN = 5

working_dir = './data/'
token_dir = './data/'
saved_path = working_dir + model_name + os.sep
model_saved_path = saved_path + 'models'
log_path = saved_path + 'logs'
model_saved_pkl_path = saved_path + 'pkl'
model_saved_graph_path = saved_path + 'graph'

# -----------------------------------------------------------------------------------------------------
# 1. Load the data for training and validation
# -----------------------------------------------------------------------------------------------------

train_total_list, train_total_list_id, train_total_list_label = dump_data_total(working_dir, 'Train')
validation_total_list, validation_total_list_id, validation_total_list_label = dump_data_total(working_dir,
                                                                                               'Validation')
test_total_list, test_total_list_id, test_total_list_label = dump_data_total(working_dir, 'Test')

total_list = train_total_list + validation_total_list + test_total_list
print(len(total_list))
# total_list is 60768

train_total_list_8_projects, train_total_list_id_8_projects, train_total_list_label_8_projects = dump_data_8_projects(
    working_dir, 'Train')
validation_total_list_8_projects, validation_total_list_id_8_projects, validation_total_list_label_8_projects = dump_data_8_projects(
    working_dir, 'Validation')

# --------------------------------------------------------------------------------------------------
# 2. Load the Tokenizer and the trained word2vec model
# --------------------------------------------------------------------------------------------------

# 2.1 Load the toknizer

train_total_list = JoinSubLists(train_total_list_8_projects)
validation_total_list = JoinSubLists(validation_total_list_8_projects)

tokenizer = LoadSavedData(token_dir + 'all_tokenizer_no_comments.pickle')

train_total_sequences = tokenizer.texts_to_sequences(train_total_list)
validation_total_sequences = tokenizer.texts_to_sequences(validation_total_list)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))
# Found 293820 unique tokens.

# print ("The length of train tokenized sequence: " + str(len(train_total_sequences)))
# print ("The length of validation tokenized sequence: " + str(len(validation_total_sequences)))

# 2.2 Load the trained word2vec model.

w2v_model_path = token_dir + 'all_w2v_model_CBOW_no_comments.txt'
w2v_model = open(w2v_model_path, encoding="utf-8")

print("-------------------------------------------------------")
print("The trained word2vec model: ")
print(glove_model)

# ----------------------------------------------------------------------------------------------------
# 3. Do the paddings.
# ----------------------------------------------------------------------------------------------------

print("max_len ", MAX_LEN)
print('Pad sequences (samples x time)')

train_total_sequences_pad = pad_sequences(train_total_sequences, maxlen=MAX_LEN, padding='post')
validation_total_sequences_pad = pad_sequences(validation_total_sequences, maxlen=MAX_LEN, padding='post')

print("The shape after paddings: ")
print(train_total_sequences_pad.shape)
print(validation_total_sequences_pad.shape)

train_set_x = train_total_sequences_pad
validation_set_x = validation_total_sequences_pad

train_set_id = train_total_list_id_8_projects
validation_set_id = train_total_list_id_8_projects

train_set_y = train_total_list_label_8_projects
validation_set_y = validation_total_list_label_8_projects

train_set_y = np.asarray(train_set_y)
validation_set_y = np.asarray(validation_set_y)

# ----------------------------------------------------------------------------------------------------
# 4. Preparing the Embedding layer
# ----------------------------------------------------------------------------------------------------

embeddings_index = {}  # a dictionary with mapping of a word i.e. 'int' and its corresponding 100 dimension embedding.

# Use the loaded model
for line in w2v_model:
    if not line.isspace():
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
w2v_model.close()

print('Found %s word vectors.' % len(embeddings_index))
# Found 82159 word vectors.

embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector


def train(train_set_x, train_set_y, validation_set_x, validation_set_y, saved_model_name):
    model = LSTM_network(MAX_LEN, EMBEDDING_DIM, word_index, embedding_matrix, True)

    callbacks_list = [
        ModelCheckpoint(
            filepath=model_saved_path + os.sep + Version + saved_model_name + '_{epoch:02d}_{val_acc:.3f}_{val_loss:3f}' + '.h5',
            monitor='val_loss', verbose=1, save_best_only=True, period=1),
        EarlyStopping(monitor='val_loss', patience=PATIENCE, verbose=1, mode="min"),
        TensorBoard(log_dir=log_path, batch_size=BATCH_SIZE, write_graph=True, write_grads=True, write_images=True,
                    embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None),
        CSVLogger(
            log_path + os.sep + saved_model_name + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log')]

    train_history = model.fit(train_set_x, train_set_y,
                              epochs=EPOCHS,
                              batch_size=BATCH_SIZE,
                              shuffle=False,
                              # The data has already been shuffle before, so it is unnessary to shuffle it again. (And also, we need to correspond the ids to the features of the samples.)
                              validation_data=(validation_set_x, validation_set_y),
                              # Validation data is not used for training (or development of the model)
                              callbacks=callbacks_list,
                              # Get the best weights of the model and stop the first raound training.
                              verbose=1)
    model.summary()
    return model, train_history


def plot_history(network_history):
    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.plot(network_history.history['loss'])
    plt.plot(network_history.history['val_loss'])
    plt.legend(['Training', 'Validation'])
    plt.savefig(model_saved_graph_path + os.sep + Version + model_name + '_Epoch_loss' + '.jpg')


#    plt.show()

if __name__ == '__main__':
    Generate_saved_path(working_dir, model_name)
    for i in range(LoopN):
        Start = Start + 1
        Version = str(Start) + '_'
        print(Version + 'th Training:')
        model, train_history = train(train_set_x, train_set_y, validation_set_x, validation_set_y, model_name)
        plot_history(train_history)
        SavedData(model_saved_pkl_path + os.sep + Version + model_name + '.pkl', train_history)
