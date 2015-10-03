#!/local/anaconda/bin/python

import numpy as np
import sys

n_h = 20

np.random.seed(seed=42)
h_a = np.random.randint(20000, size=(n_h))
h_b = np.random.randint(20000, size=(n_h))

def h(n, i):
    return (h_a[i] * n) % h_b[i]

def process(id, shingles):
    M = np.empty((n_h))
    M[:] = np.inf

    for r in shingles:
        for i in range(n_h):
            M[i] = min(M[i], h(r, i))

    key = str(list(M.astype(int)))
    print('%s\t%d' % (key, id))

for line in sys.stdin:
    line = line.strip()
    video_id = int(line[6:15])
    shingles = np.fromstring(line[16:], sep=" ").astype(int)
    process(video_id, shingles)
