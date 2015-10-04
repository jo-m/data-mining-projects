#!/local/anaconda/bin/python

import numpy as np
import sys


pycharm_mode = False


def print_duplicates(videos):
    unique = np.unique(videos)
    for i in xrange(len(unique)):
        for j in xrange(i + 1, len(unique)):
            print "%d\t%d" % (min(unique[i], unique[j]),
                              max(unique[i], unique[j]))


def my_print(videos):
    for pair in videos:
        print "%d\t%d" % (pair[0], pair[1])


def process(source):
    last_band = None
    key_count = 0
    duplicates = []
    candidate_pairs = {}
    hash_map = {}
    current_band = 0

    for line in source:
        line = line.strip()
        key, value = line.split("\t")
        band, hash_bucket, video_id = value.split(" ")
        band = int(band)
        hash_bucket = int(hash_bucket)
        video_id = int(video_id)

        if last_band is None:
            last_band = band

        if current_band != band:
            candidate_pairs[current_band] = []
            for videos in hash_map.itervalues():
                if len(videos) >= 2:
                    candidate_pairs[current_band] += [videos]
            hash_map = {}
            current_band = band

        if hash_bucket not in hash_map:
            hash_map[hash_bucket] = []

        hash_map[hash_bucket] += [video_id]

    # process last band
    candidate_pairs[current_band] = []
    for videos in hash_map.itervalues():
        if len(videos) >= 2:
            candidate_pairs[current_band] += [videos]

    for pairs in candidate_pairs.itervalues():
        for pair in pairs:
            duplicates.append((pair[0], pair[1]))

    if len(duplicates) > 0:
        my_print(duplicates)
        #print_duplicates(duplicates)

if __name__ == "__main__":
    if pycharm_mode:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("filename", help="The filename to be processed")
        args = parser.parse_args()
        if args.filename:
            with open(args.filename) as f:
                process(f)
                f.close()
    else:
        process(sys.stdin)
