#!/usr/bin/env python

import sys
import re
from operator import itemgetter

def read_sim(f):
    # Get similarity matrix in {{}}
    sim = {}
    fp = open(f, 'r')
    try:
        for line in fp:
            u1, u2, similarity = line.strip().split('\t')[:3]
            similarity = float(similarity)
            if u1 not in sim:
                sim.setdefault(u1, {})[u2] = similarity
            else:
                sim[u1][u2] = similarity
            ''' if want symmetrical matrix
            if u2 not in sim:
                sim.setdefault(u2, {})[u1] = similarity
            else:
                sim[u2][u1] = similarity
            '''
    finally:
        fp.close()
    return sim

def read_input(fp):
    users = {}
    for line in fp:
        user, url, weight = re.split('\t|,', line.strip())[:3]
        weight = int(weight)
        if user not in users:
            users.setdefault(user, {})[url] = weight
        users[user][url] = weight
    return users

def f(x1, x2):
    return x1 * x2

def main():
    '''
    Output: <user: (top k)url, score>
    '''
    k = 100
    f = 'mat_site_sim_top.loose'
    # Get similarity matrix in {{}}
    sim = read_sim(f)
    # Get users<{user:{url:weight}}>
    users = read_input(sys.stdin)
    # Reco
    user_url = {}
    for user, url_w in users.items():
        score = {}
        for url, weight in url_w.items():
            if url in sim.keys():
                for url_dest, similarity in sim[url].items():
                    if url_dest not in score:
                        score[url_dest] = weight * similarity
                    score[url_dest] += weight * similarity
        score_top = sorted(score.items(), key=itemgetter(1), reverse=1)[:k]
        for url, s in score_top:
            if user not in user_url:
                user_url.setdefault(user, {})[url] = s
            user_url[user][url] = s
            print '%s\t%s,%f' % (user, url, s)
        
if __name__ == '__main__':
    '''
    Dot
    Input:  <user: url, weight>
    Output: <user: url, score>
    '''
    main()
