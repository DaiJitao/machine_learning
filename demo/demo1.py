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


if __name__ == "__main__":
    array = [-4,0,-9,23,15,1]
    print(__max_sum(array))
