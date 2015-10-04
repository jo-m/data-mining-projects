#!/local/anaconda/bin/python

import numpy as np
import sys

pycharm_mode = True

r = 20
b = 10
k = r * b

n_shingles = 20000

np.random.seed(seed=42)
h_a = np.random.randint(1, 500, size=(k))
h_b = np.random.randint(1, 20000, size=(k))

def h(n):
    return np.mod(n * h_a, h_b)

h2_a = np.random.randint(1, 2000, size=(b, r))
h2_b = np.random.randint(1, 1000, size=(b))

def h2(M):
    M = M.reshape(b, r)
    return np.mod(np.multiply(M, h2_a).sum(axis=1) + h2_b, 100000)

def process(id, shingles):
    one_hot = np.zeros((n_shingles))
    one_hot[shingles] = 1

    M = np.empty((k))
    M[:] = np.inf

    for s in shingles:
        M = np.minimum(M, h(s))

    M = h2(M)

    for i, m in enumerate(M):
        print "%03d %06d\t%d" % (i, m, id)
    #
    # key = str(list(M.astype(int)))
    # print('%s\t%d' % (key, id))

def read_lines(source):
    for line in source:
        line = line.strip()
        video_id = int(line[6:15])
        shingles = np.fromstring(line[16:], sep=" ").astype(int)
        process(video_id, shingles)

    if pycharm_mode:
        source.close()

if __name__ == "__main__":
    if pycharm_mode:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("filename", help="The filename to be processed")
        args = parser.parse_args()
        if args.filename:
            with open(args.filename) as f:
                read_lines(f)
    else:
        read_lines(sys.stdin)

