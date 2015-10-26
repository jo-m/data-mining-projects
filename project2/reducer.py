#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import sys
import numpy as np

coef = np.loadtxt(sys.stdin)
coef = np.mean(coef, axis=0)
np.savetxt(sys.stdout, coef, newline=" ")
