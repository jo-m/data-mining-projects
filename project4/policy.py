import numpy as np
import random
from collections import defaultdict

"""
ARTICLES: (M, b) tuple for each article as a dict (key : article id)
ALPHA: parameter
LAST_RECOMMENDED: set by reccomend so `update` knows what article/user state to update for
"""
user_ndim = 6
# tuples M, M_inv, b, w
ARTICLES = defaultdict(lambda: (
    np.eye(user_ndim),
    np.eye(user_ndim),
    np.zeros(user_ndim),
    np.zeros(user_ndim),
))
LAST_RECOMMENDED = None
LAST_USER = None
LAST_USER_SQ = None
ALPHA = 0.2
MODIFIED_M = set()
MODIFIED_B = set()

def set_articles(articles_):
    pass

def update(reward):
    global ARTICLES, LAST_RECOMMENDED, LAST_USER, MODIFIED_M, MODIFIED_B
    if reward < 0:
        return
    M, _, b, _ = ARTICLES[LAST_RECOMMENDED]
    M += np.outer(LAST_USER, LAST_USER)
    M_inv = np.linalg.inv(M)
    MODIFIED_M.add(LAST_RECOMMENDED)
    if reward == 1:
        b += LAST_USER
        MODIFIED_B.add(LAST_RECOMMENDED)
    w = M_inv.dot(b)
    ARTICLES[LAST_RECOMMENDED] = (M, M_inv, b, w)

"""
z: 1 * 6 vector, user feature
articles_list: list of article ids to choose from, len ~20
"""
def reccomend(_, z, articles_list):
    global ARTICLES, LAST_RECOMMENDED, LAST_USER, LAST_USER_NORM
    LAST_USER, LAST_USER_NORM = np.array(z), np.linalg.norm(z)
    LAST_RECOMMENDED = max(articles_list, key=ucb)
    return LAST_RECOMMENDED

def ucb(article_id):
    global LAST_USER, LAST_USER_NORM, MODIFIED_M, MODIFIED_B
    z = LAST_USER

    if not article_id in MODIFIED_M:
        return ALPHA * LAST_USER_NORM
    _, M_inv, _, w = ARTICLES[article_id]
    if not article_id in MODIFIED_B:
        return ALPHA * np.sqrt(z.dot(M_inv.dot(z)))
    return np.dot(w, z) + ALPHA * np.sqrt(z.dot(M_inv.dot(z)))
