#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import os
import numpy as np
import scipy.spatial.distance as spd
from sklearn.metrics.pairwise import pairwise_distances

pycharm_mode = os.environ.get('PYCHARM_MODE')


def init_cluster_centers(points=None, k=100, method=None):
    clusters = {}
    for i in range(k):
        clusters[i] = {'center': [], 'nb_points': 0}

    if points is not None:
        if method == 'km++':
            # Choose first center uniformly at random
            centers = np.array(points[np.random.choice(points.shape[0]), :], ndmin=2)

            # Choose next centers weighted by squared distance
            for i in range(1, k):
                ds = spd.cdist(centers, points, 'sqeuclidean')
                mindist = np.min(ds, axis=0).flatten()
                idx = np.random.choice(points.shape[0], p=mindist/np.sum(mindist))
                centers = np.vstack((centers, points[idx, :]))

            for k in clusters.iterkeys():
                clusters[k]['center'] = centers[k]
        elif method == 'rand':
            # pick random points as centers
            points_index = range(len(points))
            np.random.shuffle(points_index)

            for cluster_i, point_i in enumerate(points_index[:k]):
                clusters[cluster_i]['center'] = points[point_i]
    elif method == 'rand':
        for v in clusters.itervalues():
            v['center'] = np.random.random_sample(size=(500,))

    return clusters


def assign_cluster_id(clusters, new_point):
    centers = []
    for v in clusters.itervalues():
        centers += [v['center']]

    distances = pairwise_distances(new_point, centers, metric='sqeuclidean')
    cluster_id = np.argmin(distances)

    clusters[cluster_id]['nb_points'] += 1

    return clusters, cluster_id


def recalc_center(clusters, cluster_id, new_point):
    nb_points = clusters[cluster_id]['nb_points']
    center = clusters[cluster_id]['center']
    new_center = center + float(1)/nb_points * (new_point - center)
    clusters[cluster_id]['center'] = new_center

    return clusters


def print_centers(clusters, output):
    for cluster_id, v in clusters.iteritems():
        # print('{} '.format(cluster_id)),
        np.savetxt(output, v['center'], newline=" ")
        print # prints new line


def process(input, output):
    points = None

    for line in input:
        new_point = np.fromstring(line.strip(), sep=" ")

        if points is not None:
            points = np.vstack((points, new_point))
        else:
            points = np.array(new_point, ndmin=2)

    clusters = init_cluster_centers(points=points, k=100, method='km++')

    for i in range(10):
        points_index = range(len(points))
        np.random.shuffle(points_index)

        for point_i in points_index:
            point = points[point_i]

            # assign to cluster
            clusters, cluster_id = assign_cluster_id(clusters, point)

            # recalculate center
            clusters = recalc_center(clusters, cluster_id, point)

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
