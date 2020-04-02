"""
简单的三层全连接神经网络
"""
import torch
import torch.nn as nn
from torch import optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


class SimpleNet(nn.Module):
    """
    线性全连接层
    """

    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
        super(SimpleNet, self).__init__()
        self.layer1 = nn.Linear(in_dim, n_hidden_1)  # 输入，输出
        self.layer2 = nn.Linear(n_hidden_1, n_hidden_2)  # 输入，输出
        self.layer3 = nn.Linear(n_hidden_2, out_dim)  # 输入，输出

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x


class ActivationNet(nn.Module):
    """
    非线性全连接层
    """

    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
        super(ActivationNet, self).__init__()
        self.layer1 = nn.Sequential(nn.Linear(in_dim, n_hidden_1), nn.RReLU(True))
        self.layer2 = nn.Sequential(nn.Linear(n_hidden_1, n_hidden_2), nn.RReLU(True))
        self.layer3 = nn.Sequential(nn.Linear(n_hidden_2, out_dim))

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x


class ActivationBatchNet(nn.Module):
    """
    非线性全连接层,添加了批标准化
    """

    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
        super(ActivationBatchNet, self).__init__()
        self.layer1 = nn.Sequential(nn.Linear(in_dim, n_hidden_1), nn.BatchNorm1d(n_hidden_1), nn.RReLU(True))
        self.layer2 = nn.Sequential(nn.Linear(n_hidden_1, n_hidden_2), nn.BatchNorm1d(n_hidden_2), nn.RReLU(True))
        self.layer3 = nn.Sequential(nn.Linear(n_hidden_2, out_dim))

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x


batch_size = 64
learning_rate = 1e-2
num_epoches = 20

data_tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[.5], std=[.5])])


def load_data():
    train_data = datasets.MNIST(root="./mnist", train=True, transform=data_tf, download=False)
    test_data = datasets.MNIST(root="./mnist", train=False, transform=data_tf, download=False)
    return train_data, test_data


def train():
    train_data, test_data = load_data()
    train_dataLoader = DataLoader(dataset=train_data, shuffle=True, batch_size=batch_size)
    test_dataLoader = DataLoader(dataset=test_data, shuffle=True, batch_size=batch_size)
    dense_model = SimpleNet(28 * 28, 300, 100, 10)
    if torch.cuda.is_available():
        dense_model.cuda()

    criterion = nn.CrossEntropyLoss()  # 交叉熵损失函数
    optimizer = optim.SGD(dense_model.parameters(), lr=learning_rate)
    dense_model.eval()  # 评估模式
    eval_loss = 0
    eval_acc = 0
    for data in test_dataLoader:
        img, label = data
        img = img.view(img.size(0), -1)
        if torch.cuda.is_available():
            img = Variable(img, volatile=True).cuda()
            label = Variable(label, volatile=True).cuda()
        else:
            img = Variable(img, volatile=True)
            label = Variable(label, volatile=True)

        out = dense_model(img)
        loss = criterion(out, label)
        eval_loss += loss* label
        _, pred = torch.max(out, 1)
        num_correct = (pred == label).sum()
        eval_acc += num_correct
        test_loss = eval_loss / (len(test_data))
        test_acc = eval_acc / (len(test_data))
        print("Test loss:{}, ACC:{}".format(test_loss, test_acc))


if __name__ == '__main__':
    train()
