#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:59:12 2019

@author: Seahymn
"""

from keras.models import Model
from keras.layers import Input, Dense, Embedding, GlobalMaxPooling1D, LSTM
from keras.layers.core import Dropout

LOSS_FUNCTION = 'binary_crossentropy'
# OPTIMIZER = 'adamax'
OPTIMIZER = 'sgd'

def LSTM_network(MAX_LEN, EMBEDDING_DIM, word_index, embedding_matrix, use_dropout=True):
    inputs = Input(shape=(MAX_LEN,))

    sharable_embedding = Embedding(len(word_index) + 1,
                                   EMBEDDING_DIM,
                                   weights=[embedding_matrix],
                                   input_length=MAX_LEN,
                                   trainable=False)(inputs)

    lstm_1 = LSTM(128, return_sequences=True)(sharable_embedding)  # The default activation is 'tanh',
    if use_dropout:
        droput_layer_1 = Dropout(0.5)(lstm_1)
        lstm_2 = LSTM(64, return_sequences=True)(droput_layer_1)
    else:
        lstm_2 = LSTM(64, return_sequences=True)(lstm_1)

    gmp_layer = GlobalMaxPooling1D()(lstm_2)

    if use_dropout:
        dropout_layer_2 = Dropout(0.5)(gmp_layer)
        dense_1 = Dense(64, activation='relu')(dropout_layer_2)
    else:
        dense_1 = Dense(64, activation='relu')(gmp_layer)

    dense_2 = Dense(32)(dense_1)
    dense_3 = Dense(1, activation='sigmoid')(dense_2)

    model = Model(inputs=inputs, outputs=dense_3, name='LSTM_network')

    model.compile(loss=LOSS_FUNCTION,
                  optimizer=OPTIMIZER,
                  metrics=['accuracy'])

    return model
