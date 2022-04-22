import pandas as pd
import os
import numpy as np
from keras import backend as K
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from keras.models import load_model
from SRC.Functions import dump_data_total, dump_data_8_projects, \
    LoadSavedData, JoinSubLists, Find_H5_file
from SRC.Configuration import Configuration

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

# -------------------------------------------------------------------------------------------------
# Parameters used
# --------------------------------------------------------------------------------------------------

MAX_LEN = 1000  # The Padding Length for each sample.
EMBEDDING_DIM = 100  # The Embedding Dimension for each element within the sequence of a data sample.
LOSS_FUNCTION = 'binary_crossentropy'
# OPTIMIZER = 'adamax'
OPTIMIZER = 'sgd'
BATCH_SIZE = 16

model_name = 'LSTM_8_Projects'

Start = 0
LoopN = 1  # 5

working_dir = Configuration.data_path
token_dir = Configuration.data_path
saved_path = os.path.join(working_dir, model_name)
model_saved_path = os.path.join(saved_path, 'models')

csv_path = os.path.join(saved_path, 'csv')
CSV_weight = 'prob_' + model_name + '_data_no_weight'
CSV_label = 'prob_' + model_name + '_label'
CSV_id = 'prob_' + model_name + '_id'


def test_model():
    # --------------------------------------------------------------------------------------------------
    # 1. Load the data for training and validation
    # --------------------------------------------------------------------------------------------------

    train_total_list, train_total_list_id, train_total_list_label = dump_data_total(working_dir, 'Train')
    validation_total_list, validation_total_list_id, validation_total_list_label = dump_data_total(working_dir,
                                                                                                   'Validation')
    test_total_list, test_total_list_id, test_total_list_label = dump_data_total(working_dir, 'Test')
    total_list = train_total_list + validation_total_list + test_total_list
    # print (len(total_list))
    # total_list is 60768

    test_total_list_8_projects, test_total_list_id_8_projects, test_total_list_label_8_projects = dump_data_8_projects(
        working_dir, 'Test')

    # --------------------------------------------------------------------------------------------------
    # 2. Load the Tokenizer and the trained word2vec model
    # --------------------------------------------------------------------------------------------------

    # 2.1 Load the toknizer

    test_total_list = JoinSubLists(test_total_list_8_projects)

    tokenizer = LoadSavedData(os.path.join(token_dir, 'all_matrix_no_comments.pickle'))

    test_total_sequences = tokenizer.texts_to_sequences(test_total_list)

    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    # Found 293540 unique tokens.


    # 2.2 Load the trained word2vec model.

    w2v_model_path = os.path.join(token_dir, 'mittens.txt')
    w2v_model = open(w2v_model_path, encoding="utf-8")

    print("----------------------------------------")
    print("The trained Glove model: ")
    print(glove_model)

    # --------------------------------------------------------------------------------------------------
    # 3. Do the paddings.
    # --------------------------------------------------------------------------------------------------

    print("max_len ", MAX_LEN)
    print('Pad sequences (samples x time)')

    test_total_sequences_pad = pad_sequences(test_total_sequences, maxlen=MAX_LEN, padding='post')

    print("The shape after paddings: ")

    test_set_x = test_total_sequences_pad
    test_set_id = test_total_list_id_8_projects
    test_set_y = test_total_list_label_8_projects
    test_set_y = np.asarray(test_set_y)

    # --------------------------------------------------------------------------------------------------
    # 4. Preparing the Embedding layer
    # --------------------------------------------------------------------------------------------------

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


    def test(test_set_x, test_set_y, model):
        model.compile(loss=LOSS_FUNCTION,
                      optimizer=OPTIMIZER,
                      metrics=['accuracy'])
        probs = model.predict(test_set_x, batch_size=BATCH_SIZE, verbose=1)
        predicted_classes = []
        for item in probs:
            if item[0] > 0.5:
                predicted_classes.append(1)
            else:
                predicted_classes.append(0)
        test_accuracy = np.mean(np.equal(test_set_y, predicted_classes))
        test_set_y = np.asarray(test_set_y)
        print(model_name + " classification result: ")
        target_names = ["Non-vulnerable", "Vulnerable"]  # non-vulnerable->0, vulnerable->1
        print(confusion_matrix(test_set_y, predicted_classes, labels=[0, 1]))
        print("\r\n")
        print(classification_report(test_set_y, predicted_classes, target_names=target_names))
        return probs, test_accuracy


    def ListToCSV(list_to_csv, path):
        df = pd.DataFrame(list_to_csv)
        df.to_csv(path, index=False)

    if not os.path.exists(csv_path):
        os.mkdir(csv_path)
    # test results saved in csv

    global Start
    for i in range(LoopN):
        Start = Start + 1
        Version = str(Start) + '_'
        H5_file = Find_H5_file(model_saved_path, Start)
        best_model = load_model(os.path.join(model_saved_path, H5_file))
        print(Version + 'th Testing:', H5_file)
        # The attention model is a customized model, it is needed to use a dictionary to specify it.
        probs, test_accuracy = test(test_set_x, test_set_y, best_model)
        ListToCSV(probs.tolist(), csv_path + Version + CSV_weight + '.csv')
        ListToCSV(test_set_y, csv_path + Version + CSV_label + '.csv')
        ListToCSV(test_set_id, csv_path + Version + CSV_id + '.csv')
        K.clear_session()
