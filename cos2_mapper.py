#!/usr/bin/env python

import sys

def read_input(fp):
    for line in fp:
        yield line.strip().split('\t')[:2]

def main():
    data = read_input(sys.stdin)
    for line in data:
        url, vec_len = line
        print '1\t%s,%s' % (url, vec_len)
    
if __name__ == '__main__':
    '''
    Input:  <url: vec_len>
    Output: <1: url, vec_len>
    '''
    main()