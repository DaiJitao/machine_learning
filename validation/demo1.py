import numpy as np

data = np.array([i for i in range(1, 10000)])

K = 4
np.random.shuffle(data)
samples_val = len(data) / K
results = []
for i in range(K):
    print(int(i * samples_val), int(i * samples_val + samples_val))
    examples = data[int(i * samples_val) : int(i * samples_val + samples_val)]
    results.append(examples)
print(results)
