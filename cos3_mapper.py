#!/usr/bin/env python

import sys

def read_input(fp):
    for line in fp:
        yield line.strip().split('\t')[:2]

def main():
    data = read_input(sys.stdin)
    for line in data:
        pair, y = line
        print '%s\t%s' % (pair, y)
    
if __name__ == '__main__':
    '''
    Input:  <(url1, url2): 0/1, y>
    Output: shuffle
    '''
    main()