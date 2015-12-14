#!/local/anaconda/bin/python

import numpy as np
import sys

for line in sys.stdin:
    line = line.strip()
    shingles = np.fromstring(line[16:], sep=" ").astype(int)
    print np.max(shingles)
