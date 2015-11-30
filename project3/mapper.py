#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import numpy as np
import sys
from sklearn.cluster import MiniBatchKMeans

k = MiniBatchKMeans(n_clusters=750, batch_size=1000)
X = np.loadtxt(sys.stdin)
k.fit(X)
np.savetxt(sys.stdout, k.cluster_centers_)
