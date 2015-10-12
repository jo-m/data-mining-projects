#!/local/anaconda/bin/python

import numpy as np
import sys

pycharm_mode = False

r = 50
b = 20
k = r * b # number of hash functions

n_shingles = 20000

np.random.seed(seed=42)
h_a = np.random.randint(1, 20000, size=(k))
h_b = np.random.randint(1, 20000, size=(k))

def h(n):
    return np.mod(n * h_a + h_b, n_shingles)

h2_a = np.random.randint(1, 20000, size=(b, r))
h2_b = np.random.randint(1, 20000, size=(b))

def h2(M):
    M = M.reshape(b, r)
    return np.mod(np.multiply(M, h2_a).sum(axis=1) + h2_b, 15485863)

def process(video_id, shingles):
    M = np.empty((k))
    M[:] = np.inf

    # hashing the shingles and produce the signature
    for s in shingles:
        hashed_shingle = h(s)
        M = np.minimum(M, hashed_shingle)

    # hashing the signature for this video
    M = h2(M)

    for band, hash_bucket in enumerate(M):
        print "%03d %06d\t%d\t%s" % (band, hash_bucket, video_id, shingles.tolist())
    #
    # key = str(list(M.astype(int)))
    # print('%s\t%d' % (key, id))


def read_lines(source):
    for line in source:
        line = line.strip()
        video_id = int(line[6:15])
        shingles = np.fromstring(line[16:], sep=" ").astype(int)
        process(video_id, shingles)

if __name__ == "__main__":
    if pycharm_mode:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("filename", help="The filename to be processed")
        args = parser.parse_args()
        if args.filename:
            with open(args.filename) as f:
                read_lines(f)
                f.close()
    else:
        read_lines(sys.stdin)

