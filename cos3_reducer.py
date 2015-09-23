#!/usr/bin/env python

import sys

def read_input(fp):
    for line in fp:
        yield line.strip().split('\t')[:2]

def main():
    data = read_input(sys.stdin)
    v_numerator = {}
    v_denominator = {}
    for line in data:
        x, value = line
        label, v = value.split(',')
        v = float(v)
        if label == '0':
            if x not in v_numerator:
                v_numerator[x] = v
            else:
                v_numerator[x] += v
        elif label == '1':
            v_denominator[x] = v
    # sum(product)/vec_len_prod 
    for x in v_numerator:
        if x not in v_denominator or v_denominator[x] == 0:
            y = 0
        y = v_numerator[x]/v_denominator[x]
        print '%s\t%f' % (x, y)

if __name__ == '__main__':
    '''
    Input:  <(url1, url2): 0/1, value>
    Output: <(url1, url2): cosine>
    '''
    main()
