#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys

'''
数据格式转换
'''
def character_tagging(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    
    for line in input_data.readlines():
        word_list = line.strip().split()
        for word in word_list:
            word=word.replace('/','    ')
            output_data.write(word + u"\n")
        output_data.write(u"\n")
    input_data.close()
    output_data.close()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        print ("pls use: python make_crf_train_data.py input_file output_out_file")
        # sys.exit()
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = './data/train-2.txt'
        output_file = './data/train_out.txt'
    character_tagging(input_file, output_file)
