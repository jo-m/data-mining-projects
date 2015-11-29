#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import numpy as np
import os
import sys
from sklearn.cluster import KMeans

n_clusters = int(os.environ.get('mapper__n_clusters', '100'))
n_init = int(os.environ.get('mapper__n_init', '10'))
max_iter = int(os.environ.get('mapper__n_init', '300'))

sys.stderr.write('n_clusters=%d n_init=%d max_iter=%d\n' %
                 (n_clusters, n_init, max_iter))
sys.stderr.flush()

k = KMeans(n_clusters=n_clusters,
           init='k-means++',
           n_init=10,
           max_iter=max_iter,
           tol=0.0001,
           copy_x=False,
           n_jobs=4)

X = np.loadtxt(sys.stdin)

k.fit(X)

np.savetxt(sys.stdout, k.cluster_centers_)
