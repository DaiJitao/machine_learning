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

def f(x):
    return np.exp(-np.power(x,2)/2)

if __name__ == '__main__':
    randoms = np.random.uniform(0,1,5000000)
    res = np.sum([f(x) for x in randoms])/5000000
    print(res)

    import sklearn.utils.random