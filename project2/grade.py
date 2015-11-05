#!/usr/bin/env python

score = 0.82908

easy = 0.77576
hard = 0.83011

def scale(score):
    if score > hard:
        return 1
    if score < easy:
        return 0
    return (score - easy) / (hard - easy) * 0.5 + 0.5

print scale(score)
print scale(score) * 5 + 1
