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
ALPHA = 0.15
MODIFIED_M, MODIFIED_B = set(), set()

def set_articles(articles):
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

def reccomend(_, z, articles_list):
    global ARTICLES, LAST_RECOMMENDED, LAST_USER, LAST_USER_NORM
    LAST_USER, LAST_USER_NORM = np.array(z), np.linalg.norm(z)
    LAST_RECOMMENDED = max(articles_list, key=ucb)
    return LAST_RECOMMENDED

def ucb(article_id):
    global LAST_USER, LAST_USER_NORM, MODIFIED_M, MODIFIED_B
    if not article_id in MODIFIED_M:
        return ALPHA * LAST_USER_NORM
    _, M_inv, _, w = ARTICLES[article_id]
    if not article_id in MODIFIED_B:
        return ALPHA * np.sqrt(z.dot(M_inv.dot(LAST_USER)))
    return np.dot(w, LAST_USER) + ALPHA * np.sqrt(z.dot(M_inv.dot(z)))
