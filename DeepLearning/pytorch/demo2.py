import torch

models = torch.nn.Sequential(
    torch.nn.Linear(1000, 100),
    torch.nn.ReLU(),
    torch.nn.Linear(100,10)
)

print(models)