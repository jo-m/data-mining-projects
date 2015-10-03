#!/local/anaconda/bin/python

import numpy as np
import sys

n_h = 20
max_val = 20000

np.random.seed(seed=43)
h_a = np.random.randint(1, max_val, size=(n_h))
h_b = np.random.randint(1, max_val, size=(n_h))

def h(n):
    return np.mod(n * h_a, h_b)

def process(id, shingles):
    M = np.empty((n_h))
    M[:] = np.inf

    for r in shingles:
        M = np.minimum(M, h(r))

    key = str(list(M.astype(int)))
    print('%s\t%d' % (key, id))

for line in sys.stdin:
    line = line.strip()
    video_id = int(line[6:15])
    shingles = np.fromstring(line[16:], sep=" ").astype(int)
    process(video_id, shingles)
