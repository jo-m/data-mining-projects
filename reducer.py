#!/local/anaconda/bin/python

import numpy as np
import sys


def print_duplicates(videos):
    unique = np.unique(videos)
    for i in xrange(len(unique)):
        for j in xrange(i + 1, len(unique)):
            print "%d\t%d" % (min(unique[i], unique[j]),
                              max(unique[i], unique[j]))

last_key = None
key_count = 0
duplicates = []

for line in sys.stdin:
    line = line.strip()
    key, video_id = line.split("\t")
    video_id = int(video_id)

    if last_key is None:
        last_key = key

    if key == last_key:
        duplicates.append(video_id)
    else:
        # Key changed
        print_duplicates(duplicates)
        duplicates = [video_id]
        last_key = key

if len(duplicates) > 0:
    print_duplicates(duplicates)
