#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import os
import numpy as np
import itertools
from sklearn.svm import LinearSVC
from sklearn.kernel_approximation import RBFSampler
from sklearn.kernel_approximation import AdditiveChi2Sampler

pycharm_mode = True
N_FEATURES = 400  # Dimension of the original data.
BATCH_SIZE = 30000

chi = AdditiveChi2Sampler()
chi.fit(np.zeros(N_FEATURES).ravel())
rbf = RBFSampler(gamma=1, random_state=1337, n_components=5500)
rbf.fit(np.zeros(1200).ravel())

def transform(x_original):
    return rbf.transform(chi.transform(x_original)).ravel()

def lines(source):
    for line in source:
        line = line.strip()
        (label, x_string) = line.split(" ", 1)
        label = int(label)
        x_original = np.fromstring(x_string, sep=' ')
        yield label, transform(x_original)

def main():
    if pycharm_mode:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", help="The filename to be processed", required=True)
        parser.add_argument("--output", help="The filename to be written to")
        args = parser.parse_args()
        if args.input:
            input_f = open(args.input)
            input = lines(input_f)

        if args.output:
            os.remove(args.output)
            output = open(args.output, 'a')
        else:
            output = sys.stdout
    else:
        input = lines(sys.stdin)
        output = sys.stdout

    while True:
        m = list(itertools.islice(input, 0, BATCH_SIZE))
        if len(m) == 0:
            break
        X = np.vstack([x[1] for x in m])
        Y = np.array([x[0] for x in m]).T

        clf = LinearSVC(
            fit_intercept=False,
            loss='hinge',
            C=100
        )

        clf.fit(X, Y)
        np.savetxt(output, clf.coef_)

    if pycharm_mode:
        input_f.close()
        output.close()

if __name__ == '__main__':
    main()
