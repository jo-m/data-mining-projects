import numpy as np
import random
from collections import defaultdict

"""
st: (M, b) tuple for each article as a dict (key : article id)
al: parameter alpha
last_recommended: set by reccomend so `update` knows what article/user state to update for
"""
st = None
al = 1
last_recommended = None
user_ndim = 6

def set_articles(articles_):
    global st, al, last_recommended, user_ndim
    # tuples M, b
    st = defaultdict(lambda: (
        np.eye(user_ndim),
        np.zeros(user_ndim)
    ))

"""
y: reward (-1: ignore, 1: click, 0: noclick)
"""
def update(y):
    global st, al, last_recommended, user_ndim
    if y == -1:
        return
    a, z = last_recommended
    M, b = st[a]
    # print 'update for id=', a, 'reward=', y
    M = M + np.outer(z, z)
    b = b + y * z
    st[a] = (M, b)

"""
time: int, not sequential
z: 1 * 6 vector, user feature
articles_list: list of article ids to choose from, len ~20
"""
def reccomend(time, z, articles_list):
    global st, al, last_recommended, user_ndim
    z = np.array(z)
    ucb = np.zeros(len(articles_list))
    for i, a in enumerate(articles_list):
        M, b = st[a]
        M_inv = np.linalg.inv(M)
        w = M_inv.dot(b)
        ucb[i] = np.dot(w, z) + al * np.sqrt(np.dot(z, np.dot(M_inv, z)))
    last_recommended = (articles_list[np.argmax(ucb)], z)
    return last_recommended[0]

