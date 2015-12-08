import numpy as np
import random
from collections import defaultdict

"""
ids:      n * 1 vector, article ids
articles: n * 6 matrix, article features
st: (M, b) tuple for each article as a dict (key : article id)
a: parameter alpha
last_recommended: set by reccomend so `update` knows what article/user state to update for
"""
ids, articles = None, None
st = None
a = 1
last_recommended = None

def set_articles(articles_):
    global ids, articles, st, last_recommended
    ids = np.array([a[0] for a in articles_])
    articles = np.array([a[1:] for a in articles_])
    article_n_features = articles.shape[1]
    # tuples M, b
    st = defaultdict(lambda: (
        np.eye(article_n_features),
        np.zeros(article_n_features)
    ))

"""
y: reward (-1: ignore, 1: click, 0: noclick)
"""
def update(y):
    global ids, articles, st, last_recommended
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
    global ids, articles, st, last_recommended
    z = np.array(z)
    ucb = np.zeros(len(articles_list))
    for i, a in enumerate(articles_list):
        M, b = st[a]
        M_inv = np.linalg.inv(M)
        w = M_inv.dot(b)
        ucb[i] = np.dot(w, z) + a * np.sqrt(np.dot(z, np.dot(M_inv, z)))
    last_recommended = (articles_list[np.argmax(ucb)], z)
    return last_recommended[0]

