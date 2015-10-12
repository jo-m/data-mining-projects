#!/local/anaconda/bin/python

import numpy as np
import sys
import ast
import itertools

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


def jaccard_sim(A, B):
    return float(np.setdiff1d(A, B).size) / np.union1d(A, B).size


def jaccard_d(A, B):
    return 1 - jaccard_sim(A, B)


def process(source):
    last_band = None
    duplicates = []
    non_duplicates = []
    candidate_pairs = {}
    hash_map = {}
    current_band = 0
    shingle_map = {}

    for line in source:
        line = line.strip()
        key, current_video_id, shingles = line.split("\t")
        band, hash_bucket = key.split(" ")
        band = int(band)
        hash_bucket = int(hash_bucket)
        current_video_id = int(current_video_id)
        shingles = ast.literal_eval(shingles)

        if last_band is None:
            last_band = band

        if current_band != band:
            candidate_pairs[current_band] = []
            for videos in hash_map.itervalues():
                if len(videos) >= 2:
                    candidate_pairs[current_band] += [videos]
            hash_map = {}
            current_band = band
            shingle_map = {}

        if hash_bucket not in hash_map:
            hash_map[hash_bucket] = []

        # if len(hash_map[hash_bucket]) != 0:
        #     # calc jaccard distance
        #     for v_id in hash_map[hash_bucket]:
        #         cand_pair = sorted((v_id, current_video_id))
        #
        #         if cand_pair not in non_duplicates and cand_pair not in duplicates:
        #             jd = jaccard_d(shingle_map[v_id], shingles)
        #
        #             if jd >= 0.9:
        #                 duplicates.append(cand_pair)
        #             else:
        #                 non_duplicates.append(cand_pair)

        hash_map[hash_bucket] += [current_video_id]
        #shingle_map[current_video_id] = shingles

    # process last band
    candidate_pairs[current_band] = []
    for videos in hash_map.itervalues():
        if len(videos) >= 2:
            candidate_pairs[current_band] += [videos]

    pair_hm = {}
    cp_processed = [tuple(t) for sublist in candidate_pairs.itervalues() for t in sublist] # flatten
    cp_processed = [list(itertools.combinations(t, 2)) for t in cp_processed] # combine all 2 pairs
    cp_processed = [tuple(sorted(t)) for sublist in cp_processed for t in sublist] # flatten
    for pair in cp_processed:
        pair_hm[pair] = 0 # init

    for pair in cp_processed:
        pair_hm[pair] += 1

    for pair, count in pair_hm.iteritems():
        if count >= 1:
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
