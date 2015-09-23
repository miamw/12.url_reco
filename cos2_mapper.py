#!/usr/bin/env python

import sys

def read_input(fp):
    for line in fp:
        yield line.strip().split('\t')[:2]

<<<<<<< HEAD
def main():
    data = read_input(sys.stdin)
    for line in data:
        url, vec_len = line
        print '1\t%s,%s' % (url, vec_len)
=======
def main(url_cnt):
    data = read_input(sys.stdin)
    for line in data:
        url, vec_len = line
        url = int(url)
        for i in range(url):
            print '%d,%d\t%s' % (i, url, vec_len)
        for i in range(url+1, url_cnt):
            print '%d,%d\t%s' % (url, i, vec_len)
>>>>>>> f1275ea50e1ad7be727ca4690d0f682141b9e2a3
    
if __name__ == '__main__':
    '''
    Input:  <url: vec_len>
<<<<<<< HEAD
    Output: <1: url, vec_len>
    '''
    main()
=======
    Output: <(url1, url2): vec_len>
    '''
    main(url_cnt=2188)
>>>>>>> f1275ea50e1ad7be727ca4690d0f682141b9e2a3
