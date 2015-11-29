#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np
from sklearn.cluster import KMeans

k = KMeans(n_clusters=100,
           init='k-means++',
           n_init=10,
           max_iter=300,
           tol=0.0001,
           copy_x=False)

X = np.loadtxt(sys.stdin)

k.fit(X)

np.savetxt(sys.stdout, k.cluster_centers_)
#
# sys.stderr.write('fitted a set...\n')
# sys.stderr.flush()
