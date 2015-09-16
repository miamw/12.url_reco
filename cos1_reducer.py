#!/usr/bin/env python

import sys
import math

def read_input(fp):
    for line in fp:
        yield line.strip().split('\t')[:2]

def f(weights):
    '''
    Params: weights<[]>
    Return: vec_len
    '''
    return math.sqrt(sum(x*x for x in weights))

def main():
    data = read_input(sys.stdin)
    urls = {}
    for line in data:
        url, weight = line
        weight = int(weight)
        if url not in urls:
            urls.setdefault(url, []).append(weight)
        else:
            urls[url].append(weight)
    for url, weights in urls.items():
        vec_len = f(weights)
        print '%s\t%f' % (url, vec_len)

if __name__ == '__main__':
    '''
    Input:  <url: weight>
    Output: <url: vec_len>
    '''
    main()
