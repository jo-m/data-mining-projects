#!/local/anaconda/bin/python

import numpy as np
import sys
import ast


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
    key_count = 0
    duplicates = []
    candidate_pairs = {}
    hash_map = {}
    current_band = 0

    for line in source:
        line = line.strip()
        key, band, hash_bucket, current_video_id, shingles = line.split("\t")
        band = int(band)
        hash_bucket = int(hash_bucket)
        current_video_id = int(current_video_id)
        shingles = ast.literal_eval(shingles)

        if last_band is None:
            last_band = band

        if current_band != band:
            #candidate_pairs[current_band] = []
            #for videos in hash_map.itervalues():
            #    if len(videos) >= 2:
            #        candidate_pairs[current_band] += [videos]
            hash_map = {}
            current_band = band

        if hash_bucket not in hash_map:
            hash_map[hash_bucket] = []


        video = {}
        video['id'] = current_video_id
        video['s'] = shingles

        if len(hash_map[hash_bucket]) != 0:
            # calc jaccard distance
            for video in hash_map[hash_bucket]:
                jd = jaccard_d(video['s'], shingles)
                dup_pair = sorted((video['id'], current_video_id))
                if jd >= 0.9 and dup_pair not in duplicates:
                    duplicates.append(dup_pair)

        hash_map[hash_bucket] += [video]


    # process last band
    # candidate_pairs[current_band] = []
    # for videos in hash_map.itervalues():
    #     if len(videos) >= 2:
    #         candidate_pairs[current_band] += [videos]
    #
    # for pairs in candidate_pairs.itervalues():
    #     for pair in pairs:
    #         duplicates.append((pair[0], pair[1]))

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
