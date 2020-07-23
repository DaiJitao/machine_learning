import torch

models = torch.nn.Sequential(
    torch.nn.Linear(1000, 100),
    torch.nn.ReLU(),
    torch.nn.Linear(100,10)
)

print(models)


from torch.autograd import Variable

z = Variable()
x = torch.FloatTensor([2])
x = Variable(x,requires_grad=True)
z = (x + 2) ** 2
z.backward()
print(z.data)
print(x.grad.data)