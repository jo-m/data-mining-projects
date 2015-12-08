import numpy as np
import random
from collections import defaultdict

"""
z_t: user feature
x_t: a recommendation from the set of articles
w: weight for each observed article
"""

"""
ids:      n * 1 vector
articles: n * 6 matrix
st: dict f dicts containing the state
a: parameter alpha
"""
ids, articles = None, None
st = None
a = 1

def set_articles(articles_):
    global ids, articles, st
    ids = np.array([a[0] for a in articles_])
    articles = np.array([a[1:] for a in articles_])
    article_n_features = articles.shape[1]
    # tuples M, b
    st = defaultdict(lambda: (
        np.eye(article_n_features),
        np.zeros(article_n_features)
    ))

def update(reward):
    if reward == -1: return
    # print 'update reward=%s' % str(reward)

"""
time: int, not sequencial
user_features: 1 * 6 vector
articles: list of article ids so choose from, len ~20
"""
def reccomend(time, z, articles_list):
    global ids, articles, st
    z = np.array(z)
    ucb = np.zeros(len(articles_list))
    for i, a in enumerate(articles_list):
        M, b = st[a]
        M_inv = np.linalg.inv(M)
        w = M_inv.dot(b)
        ucb[i] = np.dot(w, z) + a * np.sqrt(np.dot(z, np.dot(M_inv, z)))
    return articles_list[np.argmax(ucb)]

