#!/usr/bin/env python

import sys
import re

def read_input(fp):
    for line in fp:
        yield line.strip().split('\t')[:2]

def f(x1, x2):
    '''
    Params: weights<[]>
    Return: vec_len
    '''
    return x1 * x2

def main():
    data = read_input(sys.stdin)
    urls_prod = {}
    for line in data:
        url_pair, vec_len = line
        vec_len = float(vec_len)
        if url_pair not in urls_prod:
            urls_prod[url_pair] = vec_len
        else:
            urls_prod[url_pair] *= vec_len
    for k, v in urls_prod.items():
        print '%s\t1,%f' % (k, v)

if __name__ == '__main__':
    '''
    Input:  <(url1, url2): vec_len>
    Output: <(url1, url2): 1(numerator), vec_len1 * vec_len2>
    '''
    main()
