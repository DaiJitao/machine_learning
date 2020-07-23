from torch import nn
from torch import optim
import torch
from torch.autograd import Variable

class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(1,1)

    def forward(self, input):
        out = self.linear(input)
        return out

if torch.cuda.is_available():
    model = LinearRegression().cuda()
else:
    model = LinearRegression()

criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(),lr=1e-3)

num_epochs = 1000
for epoch in range(num_epochs):
    if torch.cuda.is_available():
        inputs = Variable(x_train).cuda()
        target = Variable(y_train).cuda()
    else:
        inputs = Variable(x_train)
        target = Variable(y_train)

    out = model(inputs)
    loss = criterion(out,target)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()



























