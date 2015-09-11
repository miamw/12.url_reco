'''
Training for Medium Site Recommendation
  
@author: Meng
'''
import os
import glob
import numpy as np
import time
from collections import Counter
from collections import defaultdict
import operator
from tld import get_tld

def util_tight_mat(mat, m, n):
    mat_tight = np.zeros((m, n))
    for l in mat:
        x, y, v = l
        mat_tight[x, y] = v
    return mat_tight

def util_load_idx(f):
    index = {}
    with open(f, 'r') as fp:
        for line in fp:
            try:
                idx, value = line.strip().split('\t')[:2]
                index[idx] = value
            except:
                print('[load_idx_site error]' + line)
    return index

def prep_data(dir_):
    '''
    Input: list_site.v1, 13_fea_user, 12_site_user_weight.f1
    Output: 
    idx_site, idx_user_train, idx_user_test 
    matrix for training: mat_site_user.loose, mat_site_user.tight
    matrix for test: mat_user_site.loose, mat_user_site.tight
    '''
    # Generate index
    def gen_idx(items, f, idx_begin=0):
        '''
        Param: 
        1. item set to index
        2. file to write
        3. index begin
        Output: idx_items
        '''
        item_dict_re = {}
        with open(os.path.join(dir_, f), 'w+') as fp:
            idx = idx_begin;
            for x in items:
                line = '{0}\t{1}\n'.format(idx, x)
                fp.write(line)
                item_dict_re[x] = idx
                idx+=1
        return item_dict_re
 
    def gen_idx_site(items, f, idx_begin=0):
        '''
        Param: 
        1. item set to index
        2. file to write
        3. index begin
        Output: idx_items
        '''
        item_dict_re = {}
        with open(os.path.join(dir_, f), 'w+') as fp:
            idx = idx_begin;
            for x in items:
                try:
                    domain = get_tld(x, as_object=True).domain
                except:
                    domain = None
                line = '{0}\t{1}\t{2}\n'.format(idx, x, domain)
                fp.write(line)
                item_dict_re[x] = idx
                idx+=1
        return item_dict_re   
    
    # Sample user
    def gen_userlists(train_step, train_perc, test_active):
        '''
        Input: 13_fea_user(sorted by cnt_active)
        Output: list_user
        '''
        f = os.path.join(dir_, '13_fea_user')
        with open(f, 'r') as fp:
            i = 0
            user_list_train = []
            user_list_test = []
            group = defaultdict(list)      
            for line in fp:
                user, cnt_site, cnt_active = line.strip().split('\t')[0:3]
                cnt_site, cnt_active = int(cnt_site), int(cnt_active)
                # User list for test
                if cnt_active >= test_active:
                    user_list_test.append(user)
                # User Sample list for training
                if cnt_site == 1:
                    continue
                elif cnt_site > 100:
                    cnt_site=100
                user_list_train.append(user)
                # Group by cnt, {group, [fea_no]}
                key = cnt_site//train_step
                group[key].append(i)
                i+=1
        # random get users for test
        idx = []
        for x in group.values():
            np.random.seed(12345)
            np.random.shuffle(x)
            ret_cnt = max(1, int(len(x)*train_perc))
            idx.extend(x[:ret_cnt])
        user_list_train = np.array(user_list_train)
        user_flt = user_list_train[idx]
        # write to file
        return user_flt, user_list_test
        
    ##### start
    # Sample_user
    user_list_train, user_list_test = gen_userlists(train_step=10, train_perc=0.1, test_active=5)
    # Index user
    user_dict_train = gen_idx(user_list_train, 'idx_user.train')
    user_dict_test = gen_idx(user_list_test, 'idx_user.test')
    # Index site
    f = os.path.join(dir_, 'list_site.v1')
    site_flt = []
    with open(f, 'r') as fp:
        for line in fp:
            line = line.strip()
            site_flt.append(line)
    site_dict = gen_idx_site(site_flt, 'idx_site')

    # Generate loose matrix: <site, user>, weight
    f = os.path.join(dir_, '12_site_user_weight.f1')
    fo_train = os.path.join(dir_, 'mat_site_user.loose')
    fo_test = os.path.join(dir_, 'mat_user_site.loose')
    mat_train_site_user_loose = []
    mat_test_user_site_loose = []
    with open(f, 'r') as fp, open(fo_train, 'w+') as fpo_train, open(fo_test, 'w+') as fpo_test:
        for line in fp:
            line = line.strip().split('\t')
            site, user, weight = line[:3]
            site_idx = site_dict[site]
            if user in user_dict_train:
                user_idx = user_dict_train[user]
                mat_train_site_user_loose.append((site_idx, user_idx, weight))
                lineo = '{0}\t{1}\t{2}\n'.format(site_idx, user_idx, weight)
                fpo_train.write(lineo)
            if user in user_dict_test:
                user_idx = user_dict_test[user]
                mat_test_user_site_loose.append((user_idx, site_idx, weight))
                lineo = '{0}\t{1}\t{2}\n'.format(user_idx, site_idx, weight)
                fpo_test.write(lineo)
    
    # Generate tight matrix
    m = len(site_dict)
    n = len(user_dict_train)
    mat = util_tight_mat(mat_train_site_user_loose, m, n)
    f = os.path.join(dir_, 'mat_site_user.tight')
    np.savetxt(f, mat, fmt='%d', delimiter='\t')

def train(dir_, start, end):
    '''
    Input: mat_site_user.tight
    Output: mat_site_sim.loose 
    '''
    # Calculate distance
    def dist(a, b):
        distances = ((a-b) ** 2).sum() ** 0.5
        return distances
    f = os.path.join(dir_, 'mat_site_user.tight')
    fo = os.path.join(dir_, 'mat_site_sim.loose')
    # Count line & init offset
    with open(f, 'r') as fp:
        line_cnt = 0
        offset_l = 0
        offset = []
        for line in fp:
            line_cnt += 1
            offset.append(offset_l)
            offset_l += len(line)
    # Get all distances     
    with open(f, 'r') as fp, open(fo, 'w+') as fpo:
        for i in range(start, min(end, line_cnt)):
            fp.seek(offset[i])
            row_no = i
            a=fp.readline()
            if not a:
                break
            for col_no, b in enumerate(fp, i+1):
                av = np.array(a.strip().split('\t'), dtype=np.int)
                bv = np.array(b.strip().split('\t'), dtype=np.int)
                distance = dist(av, bv)
                fpo.write('{0}\t{1}\t{2}\n'.format(row_no, col_no, distance))
            print('site {0} done at <{1}>'.format(row_no, time.strftime('%m-%d %H:%M:%S')))


def prep_test(dir_, site_cnt):
    '''
    Need func: util_load_idx
    Input: 
        mat_site_sim.loose
        mat_site_sim.tight, idx_site
    Return: 
        mat_site_sim_top.semi_tight, idx_site_score
    '''
    def trans_matrix(site_cnt):
        path = os.path.join(dir_, 'mat_site_sim.loose*')
        files = glob.glob(path)
        distances = np.zeros((site_cnt, site_cnt))
        for f in files:
            with open(f, 'r') as fp:
                for line in fp:
                    l = line.strip().split('\t')
                    if len(l) == 3:
                        distances[l[0], l[1]] = l[2]
        distances = distances + distances.T
        return distances
    
    def get_tops(dist, top_k):
        # relative sites sort by distance
        dist_sorted = np.zeros_like(dist)
        for i in range(len(dist)):
            dist_sorted[i] = np.argsort(dist[i])
        tops = dist_sorted[:,1:top_k+1]
        np.savetxt(os.path.join(dir_, 'mat_site_sim_top.semi_loose'), tops, fmt='%d', delimiter='\t')
        # sites score
        tops_flat = tops.flatten()
        site_cnt = Counter(tops_flat)
        site_sort = sorted(site_cnt.items(), key=operator.itemgetter(1), reverse=True)
        idx_site = util_load_idx(os.path.join(dir_, 'idx_site'))
        f = os.path.join(dir_, 'idx_site_top_score')
        with open(f, 'w+') as fp:
            for no, score in site_sort:
                no = int(no)
                try:
                    line = '{0}\t{1}\t{2}\n'.format(no, idx_site[no], score)
                    fp.write(line)
                except:
                    pass
                
    ##### start
    # Generate mat_site_sim.tight
    dist = trans_matrix(site_cnt)
    # Get top sites & site score
    get_tops(dist, top_k=100)

def test(dir_, top_k=100, user_top=50000):
    '''
    Input: idx_user.test, mat_user_site.loose, mat_site_sim_top.semi_loose
    Output: idx_user_sitelist
    '''
    def recommend(b, e, top_k):
        if e <= b:
            raise IndexError('idx_e <= idx_b!')
        users = np.zeros((e-b, sites.shape[0]))
        f = os.path.join(dir_, 'mat_user_site.loose')
        with open(f, 'r') as fp:
            for line in fp:
                line = line.strip().split('\t')[:3]
                u_idx, s_idx, weight = [int(x) for x in line]
                if b <= u_idx < e:
                    users[(u_idx-b), s_idx] = weight
        # Product
        reco = np.dot(users, sites)
        # Get top
        sort_idx = np.argsort(reco)[:, ::-1][:, :top_k]
        # Add idx_user & user
        with open(os.path.join(dir_, 'idx_user.test'), 'r') as fp_idx, open(os.path.join(dir_, 'idx_user_sitelist.ttl'), 'a') as fp_list:
            for line in fp_idx:
                line = line.strip().split('\t')[:2]
                idx, user = int(line[0]), line[1]
                if idx in range(b, e):
                    idx_user = '{0}\t{1}\t'.format(idx, user)
                    lst = ' '.join(str(x) for x in sort_idx[idx - b])
                    fp_list.write(idx_user + lst + '\n')
    # Load mat_site_sim to tight(loose.T)
    f = os.path.join(dir_, 'mat_site_sim_top.semi_loose')
    sites_semi_loose = np.loadtxt(f, dtype=np.int)
    sites = np.zeros((sites_semi_loose.shape[0], sites_semi_loose.shape[0]))    
    for i in range(sites_semi_loose.shape[0]):
        for j in range(sites_semi_loose.shape[1]):
            sites[sites_semi_loose[i, j], i] = 1
    # Recommend
    for b in range(0, user_top, 50000):
        #e = min((b + 50000), 393064)
        e = b + 50000
        recommend(b, e, top_k)
        print('{0} {1} done'.format(time.strftime('%m-%d %H:%M:%S'), e))
        
def filter_reco_list(dir_, viewed_th=10, listlen_th=20):
    '''
    Input: idx_site, mat_user_site.loose, idx_user_sitelist.ttl
    Output: idx_user_sitelist
    '''
    def get_domain():
        idx_domain = {}
        f = os.path.join(dir_, 'idx_site')
        with open(f, 'r') as fp:
            for line in fp:
                line = line.strip().split('\t')[:3]
                idx, site, domain = line
                idx_domain[idx] = domain
        return idx_domain
                
    def get_domain_skip():
        domain_skip = defaultdict(set)
        f = os.path.join(dir_, 'mat_user_site.loose')
        with open(f, 'r') as fp:
            for line in fp:
                line = line.strip().split('\t')[:3]
                user, site, cnt = line
                if int(cnt) >= viewed_th:
                    try:
                        domain = idx_domain[site]
                        domain_skip[user].add(domain)
                    except:
                        pass
        return domain_skip
    
    def filter_list():
        f = os.path.join(dir_, 'idx_user_sitelist.ttl')
        fo = os.path.join(dir_, 'idx_user_sitelist')
        with open(f, 'r') as fp, open(fo, 'w+') as fpo:
            for line in fp:
                line = line.strip().split('\t')[:3]
                idx, user, sitelist = line
                sites = sitelist.split(' ')
                sites_flt = []
                for site in sites:
                    try:
                        domain = idx_domain[site]
                    except:
                        domain = None
                    if domain not in domain_skip[idx]: 
                        sites_flt.append(site)
                        domain_skip[idx].add(domain)
                if(len(sites_flt)>0):
                    sites_flt_top = sites_flt[:20]
                    sitelist_flt = ' '.join(str(x) for x in sites_flt_top)
                    lineo = '{0}\t{1}\t{2}\n'.format(idx, user, sitelist_flt)
                    fpo.write(lineo)

    ##### Start
    idx_domain = get_domain()
    domain_skip = get_domain_skip()
    filter_list()
    
def manual_check(dir_, site_cnt=20, offset=0, mod=1000):
    '''
    Input: idx_site, mat_user_site.loose, idx_user_sitelist
    Output: check_idx_user_sitelist(user_idx, user, history, reco)
    Need func: util_load_idx
    '''
    # Load site_idx
    idx_site = util_load_idx(os.path.join(dir_, 'idx_site'))
    # Get user history sorted by actday
    f = os.path.join(dir_, 'mat_user_site.loose')
    user_histtory = defaultdict(dict)
    with open(f, 'r') as fp:
        for line in fp:
            line = line.strip().split('\t')[:3]
            user, site_no, weight = line
            user_histtory[user][site_no]=int(weight)
    user_hist = defaultdict(tuple)
    for user, sites in user_histtory.items():
        sites = tuple(site for site, weight in sorted(sites.items(), key=operator.itemgetter(1), reverse=True))
        user_hist[user] = sites
    # Write user reco list
    f = os.path.join(dir_, 'idx_user_sitelist')
    fo = os.path.join(dir_, 'check_idx_user_sitelist') 
    with open(f, 'r') as fp, open(fo, 'a+') as fpo:
        # read users already done
        user_done = set()
        for line in fpo:
            line = line.strip().split('\t')
            user_done.add(line[0])
        for line in fp:
            line = line.strip().split('\t')[:3]
            idx, user, sites = line
            # get sample
            if int(idx) % mod == offset and idx not in user_done:
                sitelist = sites.split(' ')
                for i in range(0,min(len(sitelist), site_cnt)):
                    try:
                        lineo = '{0}\t{1}\t{2}\t{3}\n'.format(idx, user, idx_site[user_hist[idx][i]], idx_site[sitelist[i]])
                    except:
                        continue
                    fpo.write(lineo)

if __name__ == '__main__':
    pass                    