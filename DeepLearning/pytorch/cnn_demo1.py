from torch import nn


class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        layer1 = nn.Sequential()
        layer1.add_module("conv1", nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1))
        layer1.add_module("relu1", nn.ReLU(True))
        layer1.add_module("pool1", nn.MaxPool2d(2, 2))
        self.layer1 = layer1

        layer2 = nn.Sequential()
        layer2.add_module("conv2", nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1))
        layer2.add_module("relu2", nn.ReLU(True))
        layer2.add_module("pool2", nn.MaxPool2d(2, 2))
        self.layer2 = layer2

        layer3 = nn.Sequential()
        layer3.add_module("conv3", nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1))
        layer3.add_module("relu3", nn.ReLU(True))
        layer3.add_module("pool3", nn.MaxPool2d(2, 2))
        self.layer3 = layer3
