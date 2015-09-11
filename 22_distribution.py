'''
import numpy as np
import matplotlib.pyplot as plot

def f(x):
    return x**3-2*x-6

x = np.linspace(-5, 5, num=100)
y = f(x)
p = plot.plot(x, y)
print(p)
'''

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from numpy import dtype

# load feature data
fea_dir = '../data/2_site_fea.demo'
fea = []
with open(fea_dir, 'r') as f:
    lineno = 0
    for line in f:
        line = line.strip().split('\t')
        if( len(line) == 12 ):
            fea.append(line)
fea = np.array(fea)
fv = fea[1:,1:].astype(float)


fv_flt = fv[np.logical_and(fv[:,0]>10, fv[:,0]<20)]
print(len(fv_flt))

exit()

n, bins, patches = plt.hist(fv[:,0], 100, normed=1, log=False, facecolor='red', alpha=0.4)
plt.subplots_adjust(left=0.15)
plt.ylabel('Probability')
plt.xlabel('Active Days')
plt.title("Histogram of Sites' Active Days")
plt.show()