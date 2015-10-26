#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np
import itertools
from sklearn.svm import LinearSVC

BATCH_SIZE = 5000

def transform(x_original):
    return x_original

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

        clf = LinearSVC(dual=False, fit_intercept=False)
        clf.fit(X, Y)
        np.savetxt(sys.stdout, clf.coef_)

if __name__ == '__main__':
    sys.stderr.write('Started a python process\n')
    main()
