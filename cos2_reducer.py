#!/usr/bin/env python

import sys
import re

def read_input(fp):
    for line in fp:
<<<<<<< HEAD
        yield re.split('\t|,', line.strip())[:3]

def get_urlpair(urls):
    '''
    Params: <iterator>urls: not sorted
    Return: [(url1, url2)]
    '''
    url1 = sorted(urls)
    url2 = url1[:]
    url_pair = []
    for i in url1:
        del url2[0]
        for j in url2:
            url_pair.append((i, j))
    return url_pair
=======
        yield line.strip().split('\t')[:2]
>>>>>>> f1275ea50e1ad7be727ca4690d0f682141b9e2a3

def f(x1, x2):
    '''
    Params: weights<[]>
    Return: vec_len
    '''
    return x1 * x2

def main():
    data = read_input(sys.stdin)
<<<<<<< HEAD
    urls = {}
    url_pair = []
    for line in data:
        url, vec_len = line[1:3]
        vec_len = float(vec_len)
        urls[url] = vec_len
        url_pair = get_urlpair(urls.keys())
    for u1, u2 in url_pair:
        y = f(urls[u1], urls[u2])
        print '%s,%s\t%d,%f' % (u1, u2, 1, y)

if __name__ == '__main__':
    '''
    Input:  <1: url, vec_len>
    Output: <(url1, url2): 1(numerator), vec_len>
=======
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
>>>>>>> f1275ea50e1ad7be727ca4690d0f682141b9e2a3
    '''
    main()
