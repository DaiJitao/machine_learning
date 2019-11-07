import numpy as np

out_features = 64
input_features = 32
timesteps = 1000

inputs = np.random.random((timesteps, input_features))
state_t = np.random.random((out_features,))

W = np.random.random((out_features, input_features))
U = np.random.random((out_features, out_features))
b = np.random.random((out_features,))
print("W=", W.shape, "x=", inputs[0].shape, "s=", state_t.shape)
dd = []
ss = []
for input in inputs:
    temp = np.dot(W, input) + np.dot(U, state_t) + b
    output_t = np.tanh(temp)
    ss.append(temp)
    dd.append(output_t)
    state_t = output_t
#
# print(np.stack(dd, axis=0))
# print(np.stack(ss, axis=0))

import pandas as pd

filePath = r"F:\pycharm_workspce\dai_github\machine_learning\DeepLearning\keras\data\jena_climate_2009_2016.csv"
data = pd.read_csv(filePath)
print(data.shape)
print(data.iloc[:, [1,2,3,4,5,6]].head())
print(data.columns)
