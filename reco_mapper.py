#!/usr/bin/env python

import sys

def read_input(fp):
    for line in fp:
        yield line.strip().split('\t')[:3]

def main():
    data = read_input(sys.stdin)
    for line in data:
        url, user, weight = line
        print '%s\t%s,%s' % (user, url, weight)
    
if __name__ == '__main__':
    '''
    Dot
    Input:  <url, user, weight>
    Output: <user: url, weight>
    '''
    main()