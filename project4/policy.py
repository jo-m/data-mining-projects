import numpy as np
from collections import defaultdict

user_ndim = 6
# tuple (M, M_inv, b, w)
ARTICLES = defaultdict(lambda: (
    np.eye(user_ndim),
    np.eye(user_ndim),
    np.zeros(user_ndim),
    np.zeros(user_ndim),
))
LAST_RECOMMENDED = None
LAST_USER = None
ALPHA = 0.125

def set_articles(articles):
    pass

def update(reward):
    global ARTICLES, LAST_RECOMMENDED, LAST_USER
    if reward < 0:
        return
    M, _, b, _ = ARTICLES[LAST_RECOMMENDED]
    M += np.outer(LAST_USER, LAST_USER)
    M_inv = np.linalg.inv(M)
    if reward == 1:
        b += LAST_USER
    w = M_inv.dot(b)
    ARTICLES[LAST_RECOMMENDED] = (M, M_inv, b, w)

def reccomend(_, z, articles_list):
    global ARTICLES, LAST_RECOMMENDED, LAST_USER
    LAST_USER = np.array(z)
    LAST_RECOMMENDED = max(articles_list, key=ucb)
    return LAST_RECOMMENDED

def ucb(article_id):
    global LAST_USER
    z = LAST_USER
    _, M_inv, _, w = ARTICLES[article_id]
    return np.dot(w, z) + ALPHA * np.sqrt(z.dot(M_inv.dot(z)))
