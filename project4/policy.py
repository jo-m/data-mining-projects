import numpy as np
import collections

# tuple (M, M_inv, b, w)
ARTICLES = collections.defaultdict(lambda: (
    np.eye(6),
    np.eye(6),
    np.zeros(6),
    np.zeros(6),
))
LAST = None
ALPHA = 0.3125

def set_articles(articles):
    pass

def update(reward):
    if reward < 0:
        return
    a, z = LAST
    M, _, b, _ = ARTICLES[a]
    M += np.outer(z, z)
    M_inv = np.linalg.inv(M)
    if reward == 1:
        b += z
    w = M_inv.dot(b)
    ARTICLES[a] = (M, M_inv, b, w)

def reccomend(_, z, articles):
    global LAST
    z = np.array(z)
    LAST = (max(articles, key=lambda k: ucb(k, z)), z)
    return LAST[0]

def ucb(article_id, z):
    _, M_inv, _, w = ARTICLES[article_id]
    return np.dot(w, z) + ALPHA * np.sqrt(z.dot(M_inv.dot(z)))
