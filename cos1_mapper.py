#!/usr/bin/env python

import sys

def read_input(fp):
    for line in fp:
        yield line.strip().split('\t')[:3]

def main():
    data = read_input(sys.stdin)
    for line in data:
        url, user, weight = line
        print '%s\t%s' % (url, weight)
    
if __name__ == '__main__':
    '''
    Input:  <url, user, weight>
    Output: <url: weight>
    '''
    main()