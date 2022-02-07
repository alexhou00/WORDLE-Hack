# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 16:28:50 2022

@author: alexhou00
"""

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

english_words = load_words()

english_words = [i for i in english_words if len(i)==5]

freq = [0 for _ in range(26)]

for word in english_words:
    for char in word:
        freq[ord(char)-ord('a')] += 1
        
suM = sum(freq)
for time in freq:
    print(time/suM*100*13/50,end=', ')#percentage*26/100