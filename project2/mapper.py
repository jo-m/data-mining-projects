#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.kernel_approximation import RBFSampler
from sklearn.kernel_approximation import AdditiveChi2Sampler

N_FEATURES = 400

chi = AdditiveChi2Sampler()
chi.fit(np.zeros(N_FEATURES).ravel())
rbf = RBFSampler(gamma=1, random_state=1337, n_components=4000)
rbf.fit(np.zeros(N_FEATURES * 3).ravel())

def transform(x_original):
    return rbf.transform(chi.transform(x_original))

def load_data():
    data = np.loadtxt(sys.stdin)
    Y = data[:, 0]
    X = data[:, 1:]
    return transform(X), Y

def main():
    X, Y = load_data()
    clf = LinearSVC(
        fit_intercept=False,
        # loss='squared_hinge',
        loss='hinge',
        # C=2.0,
    )
    clf.fit(X, Y)
    np.savetxt(sys.stdout, clf.coef_)

if __name__ == '__main__':
    main()
