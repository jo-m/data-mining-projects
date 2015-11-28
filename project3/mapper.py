#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

pycharm_mode = False


def init_cluster_centers(points, k=100):
    clusters = {}
    for i in range(k):
        clusters[i] = {'center': [], 'nb_points': 0, 'points': []}

    # pick random points as centers
    points_index = range(len(points))
    np.random.shuffle(points_index)

    for cluster_i, point_i in enumerate(points_index[:k]):
        clusters[cluster_i]['center'] = points[point_i]

    return clusters


def assign_cluster_id(clusters, new_point):
    centers = []
    for v in clusters.itervalues():
        centers += [v['center']]

    distances = pairwise_distances(new_point, centers, metric='sqeuclidean')
    cluster_id = np.argmin(distances)

    # naive approach
    #clusters[cluster_id]['points'] += [new_point]

    # not so naive approach
    clusters[cluster_id]['nb_points'] += 1

    return clusters, cluster_id


def recalc_centers(clusters, cluster_id, new_point):
    # naive approach
    #mean = np.mean(clusters[cluster_id]['points'], axis=0)

    # not so naive approach
    nb_points = clusters[cluster_id]['nb_points']
    center = clusters[cluster_id]['center']
    mean = center + float(1)/nb_points * (new_point - center)
    clusters[cluster_id]['center'] = mean

    return clusters


def print_centers(clusters, output):
    for cluster_id, v in clusters.iteritems():
        # print('{} '.format(cluster_id)),
        np.savetxt(output, v['center'], newline=" ")
        print # prints new line


def process(input, output):
    points = []

    for line in input:
        new_point = np.fromstring(line.strip(), sep=" ")
        points += [new_point]

    clusters = init_cluster_centers(points)

    for i in range(10):
        points_index = range(len(points))
        np.random.shuffle(points_index)

        for point_i in points_index:
            point = points[point_i]

            # assign to cluster
            clusters, cluster_id = assign_cluster_id(clusters, point)

            # recalculate center
            clusters = recalc_centers(clusters, cluster_id, point)

        # reset point assignment to zero
        for cluster_id in clusters.iterkeys():
            clusters[cluster_id]['nb_points'] = 0

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
