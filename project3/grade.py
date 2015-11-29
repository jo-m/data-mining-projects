#!/usr/bin/env python

score = 9.50687

easy = 13.93828
hard = 9.01981

def scale(score):
    if score < hard:
        return 1
    if score > easy:
        return 0
    return (1 - (score - hard) / (easy - hard)) * 0.5 + 0.5

print scale(score)
print scale(score) * 5 + 1
