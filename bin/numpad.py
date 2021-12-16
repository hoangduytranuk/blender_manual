#!/usr/bin/env python3
from random import randrange
number_list=[]
def genOneNumber(start, end, num_digits):
    n_str=""
    for i in range(0, num_digits):
        n = randrange(start, end+1)
        n_str += str(n)
    n_result = n_str[0:num_digits]
    return n_result

def genRangeTest(max_digits):
    for start in range (0, 9):
        for end in range(0, 9):
            n = genOneNumber(start, end, max_digits)
            print(n)

for d in range(2, 20):
    genRangeTest(d)
