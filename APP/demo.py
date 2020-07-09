
'''
Python Version： Python3.X
找出字符串的最长子串的长度，该子串中不包含重复的字符
'''
def longest_string(string):
    if string:
        if len(string) == 1:
            return 1

        str_longest = string[0]
        max_len = 1
        result_len = 0
        for chr in string[1:]:
            if chr in str_longest:
                current_len = len(str_longest)
                if current_len >= max_len:
                    max_len = current_len
                str_longest += chr
                str_longest = str_longest[str_longest.index(chr) + 1:]
            else:
                str_longest += chr
                result_len = len(str_longest)
        return max(result_len, max_len)
    return 0



if __name__ == '__main__':
    # s = 'bbbbbbbbbbb'
    s = 'rttssewet'
    print(longest_string(s))
