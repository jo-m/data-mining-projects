import numpy as np

def sim(A, B):
    return float(np.setdiff1d(A, B).size) / np.union1d(A, B).size

def d(A, B):
    return 1 - sim(A, B)
