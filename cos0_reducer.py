#!/usr/bin/env python

import sys
import re

def read_input(fp):
    for line in fp:
        yield re.split('\t|,', line.strip())[:3]

def get_urlpair(urls):
    '''
    Params: <iterator>urls: no need to be sorted, but need to be numbers
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

def f(x1, x2):
    return x1 * x2

def main():
    data = read_input(sys.stdin)
    users = {}
    # Get users<{user:{url:weight}}>
    for line in data:
        user, url, weight = line
        url, weight = int(url), int(weight)
        if user not in users:
            users.setdefault(user, {})[url] = weight
        users[user][url] = weight
    # For each user, get url pair product
    for x in users.values():
        url_pair = get_urlpair(x.keys())
        for u1, u2 in url_pair:
            y = f(x[u1], x[u2])
            print '%s,%s\t%d,%d' % (u1, u2, 0, y)

if __name__ == '__main__':
    '''
    Dot
    Input:  <user: url, weight>
    Output: <(url1, url2): 0(numerator), product>
    '''
    main()
