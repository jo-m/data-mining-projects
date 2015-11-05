#!/usr/bin/env python

score = 0.82

easy = 0.77576
hard = 0.83011

def scale(score):
    if score > hard:
        return 1
    if score < easy:
        return 0
    return (hard - score) / (hard - easy) * 0.5 + 0.5

print scale(score)
