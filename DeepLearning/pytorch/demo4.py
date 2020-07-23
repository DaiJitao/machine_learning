from torch import nn
from torch.autograd import Variable
from torch import optim

class Net(nn.Module):
    def __init__(self,in_dim,hidden1_dim):
        super(Net,self).__init__()
        self.layer = nn.Sequential(nn.Linear(in_dim,hidden1_dim), nn.ReLU(True))

