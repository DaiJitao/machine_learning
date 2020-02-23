import numpy as np

lamada = .0001
x = 2
# for i in range(10000):
#     x += lamada * np.sin(x)
#     print(x)
#
# print(x)
i = 0
while np.abs(np.sin(x)) >= 0.000000000002:
    x += lamada * np.sin(x)
    i += 1
    print("i=", i, " ", x)
