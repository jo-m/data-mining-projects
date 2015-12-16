#!/usr/bin/env python

score = 0.06641

easy = 0.044115
hard = 0.065825

def scale(score):
    if score > hard:
        return 1
    if score < easy:
        return 0
    return (1 - (hard - score) / (hard - easy)) * 0.5 + 0.5

print scale(score)
print scale(score) * 5 + 1
