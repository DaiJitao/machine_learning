import numpy as np


class HiddenMarkovModel(object):
    def __init__(self, _pi, state_transitions, observations):
        '''

        :param _pi: 初始状态概率向量 numpy.array (n,) 状态长度n
        :param A: 状态转移矩阵 numpy.array (n,n) 状态长度n
        :param B: 观测概率矩阵 numpy.array (n,m) 状态长度n,观测集合长度为m

        '''
        self._pi = _pi
        self.A = state_transitions
        self.B = observations

    def predict(self, sequences):
        '''

        :param sequences: 已知观测序列 {0,1,2,1,2,0,...}
        :return:
        '''
        if sequences and len(sequences) != 0:
            observation = sequences[0]
            # 获取状态集合长度
        return None
