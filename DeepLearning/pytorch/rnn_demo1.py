from torch import nn
from torch.autograd import Variable
import torch
import numpy as np


batch_size = 2
max_length = 3
hidden_size = 2
n_layers = 1

# 这个RNN由两个全连接层组成，对应的两个hidden_state的维度是2，输入向量维度是1
# batch_first – If True, then the input and output tensors are provided as (batch, seq, feature). Default: False
rnn = nn.RNN(1, hidden_size, n_layers, batch_first=True) #
#
x = torch.FloatTensor([[1, 0, 0], [1, 2, 3]]).resize_(2, 3, 1)
x = Variable(x)  # [batch, seq, feature], [2, 3, 1]
print(x)

seq_lengths = np.array([1, 3])
# 对seq_len进行排序
order_idx = np.argsort(seq_lengths)[::-1]