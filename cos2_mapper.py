#!/usr/bin/env python

import sys

def read_input(fp):
    for line in fp:
        yield line.strip().split('\t')[:2]

def main(url_cnt):
    data = read_input(sys.stdin)
    for line in data:
        url, vec_len = line
        url = int(url)
        for i in range(url):
            print '%d,%d\t%s' % (i, url, vec_len)
        for i in range(url+1, url_cnt):
            print '%d,%d\t%s' % (url, i, vec_len)
    
if __name__ == '__main__':
    '''
    Input:  <url: vec_len>
    Output: <(url1, url2): vec_len>
    '''
    main(url_cnt=2188)