import torch

class LineRegression(torch.nn.Module):

    def __init__(self):
        super(LineRegression, self).__init__()
        self.linear = torch.nn.Linear(1,1)

    def forward(self,x):
        out = self.linear(x)
        return out

if __name__ == '__main__':
    model = LineRegression()

    # 定义损失函数
    loss = torch.nn.MSELoss()

    # 定义优化器
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # 训练模型
    num_epoches = 1000
    for epach in range(num_epoches):

