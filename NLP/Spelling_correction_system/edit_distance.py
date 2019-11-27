'''
字符串的编辑距离
'''
from Levenshtein import StringMatcher
import Levenshtein
import numpy as np

def edit_distance(src: str, target: str):
    if src == None or target == None:
        return None
    len_src = len(src)
    len_target = len(target)
    if len_src == 0 or len_target == 0:
        return max(len_src, len_target)

    else:
        max_len = max(len_target, len_src)
        t = [0] * (max_len+1)
        d = [t] * (max_len+1)
        temp_distance = 0
        for i in range(1, len_src + 1):
            for j in range(1, len_target + 1):
                if src[i-1] == target[j-1]:
                    temp_distance = 0
                else:
                    temp_distance = 1
                d[i][j] = min(d[i][j - 1]+1, d[i - 1][j] + 1,d[i-1][j-1]+temp_distance)
        print(d)
        return d[len_src][len_target]

d = edit_distance("dai22222222", "dai")
print(np.max(d))
c = Levenshtein.distance("dai2", "123")
print(c)