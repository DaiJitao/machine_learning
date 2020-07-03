
import torch
import torch.nn as nn
from torch.nn import Parameter
from torch.nn import init
from torch import Tensor
import math

'''
https://blog.csdn.net/CVSvsvsvsvs/article/details/90300647?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-4.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-4.nonecase
'''

class NaitiveLSTM(nn.Module):
    def __init__(self, input_size):
        pass