# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 15:21:39 2022

@author: alexhou00
"""

import re
from wordfreq import word_frequency
from random import choice, sample, randint

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def rank_words(word):
    score = word_frequency(word,'en')
    for letter in set(word):
        score *= letterfreq[ord(letter)-ord('a')]
    return score

def ask(question):
    sentence = input(question)
    sentence = ' '+sentence.lower()+' '
    tr_table = dict(zip(map(ord,u'０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'),
                     map(ord,u'0123456789abcdefghijklmnopqrstuvwxyz')))
    sentence = sentence.translate(tr_table)
    certainty = 1
    saying_yes = (' y ','yes','yeah','of course','absolute','definite','won','win','yep','yup','yay',
                  'ya','sure','totally','certainly','undoubtedly','yea','uh-huh','hmm',u'\u1F44D','aye',
                  'ok','o.k','o k')
    saying_no = (' n ','no','lose', 'n\'t','lost','yeah right', 'hardly', 'nah', 'pass')
    for phr in saying_yes:
        if phr in sentence:
            certainty*=2
    for phr in saying_no:
        if phr in sentence:
            certainty*=-2
    return certainty

english_words = load_words()
haveToContinue = True
letterfreq = [2.7414499308958415, 0.6824224148762407, 0.8963940193491644, 0.9182811911044102, 
              2.5480588013569543, 0.40442266616409095, 0.6438748586505842, 0.7461238849101646, 
              1.6552581982661139, 0.12282950119361731, 0.5693931398416886, 1.3870586757130294, 
              0.814725468023621, 1.320743812036688, 1.704912677472044, 0.7510239979896971, 
              0.045407714537002125, 1.6800854378690793, 2.135469280060309, 1.3684382460108053, 
              1.0979520040206057, 0.28681995225530843, 0.38253549440884543, 0.11792938811408468, 
              0.8235456715667797, 0.15484357331323031]  #percentage*26/100

try: n = int(input("Number of letters:"))
except: print("Unknown Error Occured, number set to 5");n=5
possible_words = [i for i in english_words if len(i)==n]
possible_words = sorted(possible_words, key=lambda x : rank_words(x), reverse=True)
black_letters = set()

suggest = ask("Want me to suggest any word to start? ")
num_rand = randint(5, 15)
if suggest>1:
    print("Recommended Words:")
    print(*sample(possible_words[:num_rand], num_rand))

while (haveToContinue):
    counts = [0 for i in range(26)]
    possible_words = sorted(possible_words, key=lambda x : rank_words(x), reverse=True)
    #get green letters
    reg_input = ''
    while len(reg_input) != n:
        reg_input = input("\nEnter green letters with wildcards (regex):").lower()
    reg = re.compile(reg_input) #example: "l..st" --> least
    for l in [m for m in reg_input if m!='.']:
        counts[ord(l)-ord('a')]+=1
    #get yellow letters and their position
    contains = (input("Enter yellow letters with their indexes:").lower()).split() #example: e2 a3
    contains = {(j[0],j[1:]) for j in contains}
    for l,m in contains:
        counts[ord(l)-ord('a')]+=1
    #get black letters
    black_letters = black_letters.union(set(input("Enter black letters:").lower()))
  
    
    #find possible words
    possible_words_fixed = possible_words.copy() 
    toPrint = []
    for word in possible_words_fixed:
        match_green = bool(re.match(reg, word))
        if (match_green) and \
           (all(j in word and word[int(k)-1]!=j for j,k in contains)) and \
           (all(word.count(m)<=counts[ord(m)-ord('a')] for m in black_letters)):
            toPrint.append(word)
        else: possible_words.remove(word)
    
    #print results
    numPrint = (input("There are %d possible words, print how many out? (all/num/0):" % len(toPrint))).lower()
    if numPrint=='all': numPrint = len(toPrint)
    elif numPrint == '': numPrint = 0
    else: numPrint = int(numPrint)
    print("\nPossible words sorted by possibility:")
    cnt = 0
    for word in toPrint[:numPrint]:
        print(word, end=' '*3)
        cnt += 1
        if cnt>=(60-3*(n-1))/5: print();cnt=0
    haveToContinue = (ask("\nContinue? ")>1)

certainty = ask("Did you win? ")
if certainty>1:
    print("\n%s%s \n%s"%
          (choice(('Congratulations','Congrats', "Hooray", "Yay")),
           choice(('!','!!', '!!!', '.')),
           choice(("I bet you're satisfied with my job.","Did I do a great job?",
                   "Did you enjoy the WORDLE game with my help?","Come again next time!"))))
elif certainty<0:
    print("%s%s \n%s"%
          (choice(('Oops','Uh oh', "Oh", "Nah nevermind")),
           choice(('...',' sorry.', ' I\'m sorry...', '.')),
           choice(("Better luck next time.","You can help the author improve the code, though.",
                   "Any suggestions for me to improve?","Try again next time!"))))
    
    
    