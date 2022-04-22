import os
from SRC import movefiles
from SRC.utils import RemoveCommentsAndBlanks
from SRC import LoadCFilesAsText
from SRC import Embedding
from SRC.Configuration import Configuration
from SRC import Train_model
from SRC import Test_model

# make folder and move files
# 1.执行movefiles.py 将所有数据按照6:2:2的比例分为Train, Validation, Test
data_folder_list = movefiles.make_dir_and_move_files()


# remove comment in c files
# 2.执行 removeComments_Blanks.py 将所有漏洞函数文件中的comments去掉
for sub_list in data_folder_list:
    for folder_path in sub_list:
        RemoveCommentsAndBlanks.func_comment_remove(folder_path)


# 3.执行 LoadCFilesAsText.py 将c文件分割为Word，非漏洞函数文件标记为0，漏洞函数文件标记为1，将结果保存为.pkl文件
LoadCFilesAsText.generate_pkl(Configuration.data_path, 'Train')
LoadCFilesAsText.generate_pkl(Configuration.data_path, 'Validation')
LoadCFilesAsText.generate_pkl(Configuration.data_path, 'Test')


# 4.执行 Embedding.py ，word2vector将Word转换为向量，保存为.tx，t和.pkl文件
Embedding.do_embed()



# 5.设计模型，模型保存文件如LSTM_model_GPU.py 

# 6.Function.py文件中保存Train和Test需要用到的所有函数。本次实验将9个Projects分为两部分进行测试，
# 其中Xen由于是函数之间相互调用产生漏洞，所以单独列出，其余8个Projects属于单独的函数调用产生漏洞。

# 7.训练模型
Train_model.train_model()

# 8.Train model 训练完模型后找到最好的 .h5（模型存放文件）在Test model中更改best_model的值，再执行Test model
Test_model.test_model()
