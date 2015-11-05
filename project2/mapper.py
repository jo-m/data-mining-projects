#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np
import itertools
from sklearn.svm import LinearSVC
from sklearn.kernel_approximation import RBFSampler
from sklearn.kernel_approximation import AdditiveChi2Sampler

BATCH_SIZE = 30000
N_FEATURES = 400

chi = AdditiveChi2Sampler()
chi.fit(np.zeros(N_FEATURES).ravel())
rbf = RBFSampler(gamma=1, random_state=1337, n_components=4500)
rbf.fit(np.zeros(1200).ravel())

def transform(x_original):
    return rbf.transform(chi.transform(x_original)).ravel()

def lines():
    for line in sys.stdin:
        line = line.strip()
        (label, x_string) = line.split(" ", 1)
        label = int(label)
        x_original = np.fromstring(x_string, sep=' ')
        yield label, transform(x_original)

def main():
    input = lines()
    while True:
        m = list(itertools.islice(input, 0, BATCH_SIZE))
        if len(m) == 0:
            break
        X = np.vstack([x[1] for x in m])
        Y = np.array([x[0] for x in m]).T

        clf = LinearSVC(
            fit_intercept=False,
            loss='hinge'
        )
        clf.fit(X, Y)
        np.savetxt(sys.stdout, clf.coef_)

if __name__ == '__main__':
    main()
