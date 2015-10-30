#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np

pycharm_mode = False


def process(input, output):
    coef = np.loadtxt(input)
    coef = np.mean(coef, axis=0)
    np.savetxt(output, coef, newline=" ")

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
