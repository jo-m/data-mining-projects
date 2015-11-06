#!/usr/bin/env python

import numpy as np
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler

# calculate mean and stdev for use in transformation

X = np.loadtxt('data/training_sub.txt')[:, 1:]
s = StandardScaler()
s.fit(X)
print s.mean_
print s.std_
