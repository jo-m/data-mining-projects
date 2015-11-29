#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import numpy as np
import os
import sys
from sklearn.cluster import KMeans

n_clusters = int(os.environ.get('mapper__n_clusters', '500'))
n_init = int(os.environ.get('mapper__n_init', '10'))
sys.stderr.write('n_clusters=%d n_init=%d\n' %
                 (n_clusters, n_init))

k = KMeans(n_clusters=n_clusters,
           n_init=n_init,
           copy_x=False)

X = np.loadtxt(sys.stdin)

k.fit(X)

np.savetxt(sys.stdout, k.cluster_centers_)
