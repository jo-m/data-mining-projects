#!/local/anaconda/bin/python

import numpy as np
import sys

def process(id, shingles):
    # print(id, shingles)
    key = str(shingles.shape)
    print('%s\t%d' % (key, id))

if __name__ == "__main__":
    np.random.seed(seed=42)

    for line in sys.stdin:
        line = line.strip()
        video_id = int(line[6:15])
        shingles = np.fromstring(line[16:], sep=" ")
        process(video_id, shingles)
