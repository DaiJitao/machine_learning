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
        d = [[0] * len_target for i in range(len_src)]  # len_src*len_target
        for i in range(1, len_src + 1):
            for j in range(1, len_target + 1):
                if src[i - 1] == target[j - 1]:
                    d[i][j] = d[i - 1][j - 1]
                else:
                    d[i][j] = d[i - 1][j - 1] + 1
        print(d)
        return d[len_src - 1][len_target - 1]


word1 = "122"
word2 = "1212"
d = edit_distance(word1, word2)
print(d)
c = Levenshtein.distance(word1, word2)
print(c)
