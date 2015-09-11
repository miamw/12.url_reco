import os

def mapping_mat(dir_):
    '''
    Input: idx_site, idx_site.old, mat_site_dist_split.*
    Output: mat_site_sim_old.loose, idx_site.map
    '''
    # Read new dict: {value: idx}
    f = os.path.join(dir_, 'idx_site')
    idx_new = {}
    with open(f, 'r') as fp:
        for line in fp:
            idx, value = line.strip().split('\t')[:2]
            idx_new[value] = idx
    # Read old dict: {idx_o: idx_n}
    f = os.path.join(dir_, 'idx_site.old')
    fo = os.path.join(dir_, 'idx_site.map')
    idx_map = {}
    with open(f, 'r') as fp, open(fo, 'w+') as fpo:
        for line in fp:
            idx, value = line.strip().split('\t')[:2]
            site = 'http://' + value
            if site in idx_new:
                idx_map[idx] = idx_new[site]
                lineo = '{0}\t{1}\n'.format(idx, idx_new[site])
                fpo.write(lineo)
    # Get new mat
    f = os.path.join(dir_, 'v1/mat_site_dist')  
    fo = os.path.join(dir_, 'mat_site_sim.loose.old')
    with open(f, 'r') as fp, open(fo, 'w+') as fpo:
        for line in fp:
            line = line.strip().split('\t')
            if len(line) == 3:
                x, y, v = line
                if x in idx_map and y in idx_map:
                    lineo = '{0}\t{1}\t{2}\n'.format(idx_map[x], idx_map[y], v)
                    fpo.write(lineo)
                else:
                    l = '{0}\t{1}\t{2}'.format(x, y, v)
                    print(l) 
    
if __name__ == '__main__':
    mapping_mat('../data/')