#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import os
import numpy as np
import scipy.spatial.distance as spd
from sklearn.metrics.pairwise import pairwise_distances

pycharm_mode = os.environ.get('PYCHARM_MODE')


def init_cluster_centers(points=None, k=100, method=None, point_length=0):
    cluster_centers = np.zeros(shape=(k, point_length))
    cluster_nb_points = np.zeros(shape=(k,), dtype=np.int)

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

            cluster_centers = centers
            cluster_nb_points = np.ones(shape=(k,), dtype=np.int)
        elif method == 'rand':
            # pick random points as centers
            points_index = range(len(points))
            np.random.shuffle(points_index)

            for cluster_i, point_i in enumerate(points_index[:k]):
                cluster_centers[cluster_i] = points[point_i]
    elif method == 'rand':
        cluster_centers = np.random.random_sample(size=(k, point_length))

    return cluster_centers, cluster_nb_points


def assign_cluster_id(cluster_centers, cluster_nb_points, new_point):
    distances = pairwise_distances(new_point, cluster_centers, metric='sqeuclidean')
    cluster_id = np.argmin(distances)
    cluster_nb_points[cluster_id] += 1

    return cluster_centers, cluster_nb_points, cluster_id


def recalc_center(cluster_centers, cluster_nb_points, cluster_id, new_point):
    nb_points = cluster_nb_points[cluster_id]
    center = cluster_centers[cluster_id]
    new_center = center + float(1)/nb_points * (new_point - center)
    cluster_centers[cluster_id] = new_center

    return cluster_centers


def print_centers(cluster_centers, output):
    for center in cluster_centers:
        # print('{} '.format(cluster_id)),
        np.savetxt(output, center, newline=" ")
        print # prints new line


def process(input, output):
    k = 1000
    point_length = 500
    cluster_centers, cluster_nb_points = init_cluster_centers(k=k, point_length=point_length)

    for i, line in enumerate(input):
        new_point = np.fromstring(line.strip(), sep=" ")

        # take the first k points as cluster centers
        if i < k:
            cluster_centers[i] = new_point
            cluster_nb_points[i] += 1
        else:
            # assign to cluster
            cluster_centers, cluster_nb_points, cluster_id = assign_cluster_id(cluster_centers, cluster_nb_points, new_point)

            # recalculate center
            cluster_centers = recalc_center(cluster_centers, cluster_nb_points, cluster_id, new_point)

    print_centers(cluster_centers, output)


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
