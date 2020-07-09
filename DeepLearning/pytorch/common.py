import torch

BATCH_SIZE = 16
EPOCHS = 4
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(DEVICE)