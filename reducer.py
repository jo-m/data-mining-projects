#!/local/anaconda/bin/python

import numpy as np
import sys
import ast
import itertools

pycharm_mode = False

matching_bands = 6

def my_print(videos):
    for pair in videos:
        print "%d\t%d" % (pair[0], pair[1])


def jaccard_sim(A, B):
    return float(np.setdiff1d(A, B).size) / np.union1d(A, B).size


def jaccard_d(A, B):
    return 1 - jaccard_sim(A, B)


def process(source):
    duplicates = []
    candidate_pairs = {}

    for line in source:
        line = line.strip()
        key, current_video_id = line.split("\t")
        band, bucket, succ_band, succ_bucket = key.split(" ") # bucket <= succ_bucket
        band = int(band)
        bucket = int(bucket)
        succ_band = int(succ_band)
        succ_bucket = int(succ_bucket)
        current_video_id = int(current_video_id)

        if band not in candidate_pairs:
            candidate_pairs[band] = {}

        if succ_band not in candidate_pairs:
            candidate_pairs[succ_band] = {}

        if bucket not in candidate_pairs[band]:
            candidate_pairs[band][bucket] = []

        if succ_bucket not in candidate_pairs[succ_band]:
            candidate_pairs[succ_band][succ_bucket] = []

        if current_video_id not in candidate_pairs[band][bucket]:
            candidate_pairs[band][bucket] += [current_video_id]

        if current_video_id not in candidate_pairs[succ_band][succ_bucket]:
            candidate_pairs[succ_band][succ_bucket] += [current_video_id]

    pair_hm = {}
    cp_processed = [videos for band_hm in candidate_pairs.itervalues() for videos in band_hm.itervalues() if len(videos)>=2] # flatten
    cp_processed = [tuple(t) for t in cp_processed]
    cp_processed = [list(itertools.combinations(t, 2)) for t in cp_processed] # combine all 2 pairs
    cp_processed = [tuple(sorted(t)) for sublist in cp_processed for t in sublist] # flatten
    for pair in cp_processed:
        pair_hm[pair] = 0 # init

    for pair in cp_processed:
        pair_hm[pair] += 1

    for pair, count in pair_hm.iteritems():
        if count >= matching_bands:
            duplicates.append(pair)

    if len(duplicates) > 0:
        my_print(duplicates)

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
