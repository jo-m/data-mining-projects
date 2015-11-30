#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import numpy as np
import sys
from sklearn.cluster import KMeans

k = KMeans(n_clusters=100, n_init=15, copy_x=False)
X = np.loadtxt(sys.stdin)
k.fit(X)
np.savetxt(sys.stdout, k.cluster_centers_)
