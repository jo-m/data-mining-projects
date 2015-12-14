#!/local/anaconda/bin/python

import numpy as np
import sys

pycharm_mode            = False
dani_formatted_output   = True
output_shingles           = True

# compare slide-deck3 page 32 for selection of r and b.
r = 20
b = 50
k = r * b # number of hash functions

n_shingles = 20000

large_prime = 1087 # shouldn't this number be smaller than n_shingles to hash to a smaller
                        # amount of buckets than the amount of shingles?

np.random.seed(seed=42)
h_a = np.random.randint(1, 1087, size=(k))     # try smaller upper bound than 20000 later..
h_b = np.random.randint(1, 1087, size=(k))

def h(n):
    return np.mod(n * h_a + h_b, n_shingles)

h2_a = np.random.randint(1, 1087, size=(b, r))
h2_b = np.random.randint(1, 1087, size=(b))

def h2(M):
    M = M.reshape(b, r)
    return np.mod(np.multiply(M, h2_a).sum(axis=1) + h2_b, large_prime)

def process(id, shingles):
    M = np.empty((k))
    M[:] = np.inf

    # hashing the shingles and produce the signature
    # for reference: http://infolab.stanford.edu/~ullman/mmds/ch3.pdf
    for s in shingles:
        hashed_shingle = h(s) 
        # vector, each row contains the shingle hashed with one of the hashfuctins
        M = np.minimum(M, hashed_shingle)   #update signature vector (k-dimensional)
        H = M.astype(int)

    # hashing the signature for this video
    M = h2(M).astype(int)   #update signature vector (b-dimensional now)

    # loop over all (band, bucket) in M
    if dani_formatted_output: # id, buckets, shingles
        s = str(id) + ' - ' + str(M.tolist()).strip('[]')
        if output_shingles:
	        s = s + ' - ' + str(shingles.astype(int).tolist()).strip('[]')
        print s.replace(',','')
    else:
	    for (band, bucket) in enumerate(M):
	        print "%03d %06d\t%d-%s" % (band, bucket, id, shingles.tolist())

def read_lines(source):
    for line in source:
        line = line.strip()
        video_id = int(line[6:15])
        shingles = np.fromstring(line[16:], dtype=int, sep=" ")    # stored into array
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
