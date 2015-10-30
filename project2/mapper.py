#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np
import itertools
from sklearn.svm import LinearSVC

pycharm_mode = False

BATCH_SIZE = 5000

def transform(x_original):
    return x_original

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
            output = args.output
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
            loss='hinge'
        )
        clf.fit(X, Y)
        np.savetxt(output, clf.coef_)

    if pycharm_mode:
        input_f.close()

if __name__ == '__main__':
    main()
