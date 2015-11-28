#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

pycharm_mode = False


def init_cluster_centers(k=100):
    clusters = {}
    for i in range(k):
        clusters[i] = {'center': [], 'nb_points': 0}

    for v in clusters.itervalues():
        v['center'] = np.random.random_sample(size=(500,))

    return clusters


def assign_cluster_id(clusters, new_point):
    centers = []
    for v in clusters.itervalues():
        centers += [v['center']]

    distances = pairwise_distances(new_point, centers, metric='sqeuclidean')
    cluster_id = np.argmin(distances)

    # naive approach
    # clusters[cluster_id]['points'] += [new_point]

    # not so naive approach
    clusters[cluster_id]['nb_points'] += 1

    return clusters, cluster_id


def recalc_centers(clusters, cluster_id, new_point):
    # naive approach
    # mean = np.mean(clusters[cluster_id]['points'], axis=0)

    # not so naive approach
    nb_points = clusters[cluster_id]['nb_points']
    center = clusters[cluster_id]['center']
    mean = center + float(1/nb_points) * (new_point - center)
    clusters[cluster_id]['center'] = mean

    return clusters


def print_centers(clusters, output):
    for cluster_id, v in clusters.iteritems():
        # print('{} '.format(cluster_id)),
        np.savetxt(output, v['center'], newline=" ")
        print # prints new line


def process(input, output):
    clusters = init_cluster_centers()

    for line in input:
        new_point = np.fromstring(line.strip(), sep=" ")

        # assign to cluster
        clusters, cluster_id = assign_cluster_id(clusters, new_point)

        # recalculate center
        clusters = recalc_centers(clusters, cluster_id, new_point)

    print_centers(clusters, output)


if __name__ == "__main__":
    if pycharm_mode:
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--input", help="The filename to be processed", required=True)
        parser.add_argument("--output", help="The filename to be written to")
        args = parser.parse_args()
        if args.input:
            with open(args.input) as f:
                process(f, args.output if args.output else sys.stdout)
                f.close()

    else:
        process(sys.stdin, sys.stdout)
