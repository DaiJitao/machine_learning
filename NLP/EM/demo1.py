import numpy as np

A_pos = 0.71
B_pos = 0.58
all_ = 10


def count(A_pos_count, B_pos_count):
    prop_A = np.power(A_pos, A_pos_count) * np.power(1 - A_pos, all_ - A_pos_count)
    prop_B = np.power(B_pos, B_pos_count) * np.power(1 - B_pos, all_ - B_pos_count)
    p_A = prop_A / (prop_A + prop_B)
    p_B = prop_B / (prop_A + prop_B)
    return p_A, p_B


print(count(9, 9))
