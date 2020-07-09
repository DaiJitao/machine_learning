import torch
from torch import nn

from torch.autograd import Variable
print(torch.__version__)
embeds = nn.Embedding(2, 5)
torch.manual_seed(1)
print(embeds.weight)

context_size = 2 # 上下文的大小，即窗口大小

lr = 1e-2