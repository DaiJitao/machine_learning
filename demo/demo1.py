import time


def printDemo():
    isFlag = True
    count = 0
    while isFlag:
        count += 1
        if count == 100000:
            isFlag = False


def __max_sum(array):
    '''
    最大连续子数组的和
    :param array:
    :return:
    '''
    size = len(array)
    if size == 1:
        return array[0]

    max_sum = [0] * len(array)
    max_sum[0] = array[0]
    current_sum = 0

    for i in range(1, size):
        p2 = max_sum[i - 1] + array[i]
        max_sum[i] = max(0, p2)
        if max_sum[i] > current_sum:
            current_sum = max_sum[i]
    return max_sum, current_sum


"""
https://leetcode-cn.com/problems/two-sum/
"""


class Solution4(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # 建立一个字典
        d = dict()
        for index, i in enumerate(nums):
            key = str(i)
            if key in d:
                d.get(key).append(index)
            else:
                d.update({key: [index]})
            index += 1
        r = []
        for index, i in enumerate(nums):
            t = target - int(i)
            tKey = str(t) # 目标值
            if tKey in d:
                indexLst = d.get(tKey)
                # 删除重复元素
                indexLstCopy = indexLst[:]
                if index in indexLstCopy:
                    indexLstCopy.remove(index)
                r.extend(indexLstCopy)
        return r





if __name__ == "__main__":
    solution = Solution4()
    l = [3,2,4]
    # [[1,4],[4,5]] # [[1,3],[2,6],[8,10],[15,18]]
    s = solution.twoSum(l,6)
    print(s)
