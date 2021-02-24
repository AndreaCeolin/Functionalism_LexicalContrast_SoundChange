#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script has been used perform functional load calculations on the English (UK) CHILDES data.

author: Andrea Ceolin
date: February 2021
'''

'''
Get the token frequencies of the corpus
'''

from collections import Counter
import math


words_tokens = Counter()
for line in open('french_corpus.txt', 'r'):
    word, counts = line.split()
    words_tokens[word] += int(counts)

print(sum(words_tokens.values()))

'''
Get the type frequencies of the corpus
The number of types is lower than 5000, because of homophones
'''

words_types = {key:1 for key in words_tokens}

print(sum(words_types.values()))

'''
These are the three main functions to extract ngrams and calculate entropy loss
'''

def ngrams(words_dic, k):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param k: the order of the Markov model
    :return: ngram counts
    '''
    counts = Counter()
    if k == 0:  #return unigrams if k=0
        for word in words_dic:
            for index, letter in enumerate(word):
                counts[word[index]] += words_dic[word]
    else: #return k+1grams if k>1
        for word in words_dic:
            padded_word = "|" + word + "|"
            for index, letter in enumerate(padded_word[:-k]):
                counts[padded_word[index:index+k+1]] += words_dic[word]
    return counts

def entropy(words_dic, k=2):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param k: the order of the Markov model
    :return: entropy
    '''
    ngrams_dic = ngrams(words_dic, k) #retrieves ngrams
    total = sum(ngrams_dic.values()) #ngram total
    sommation = 0
    for value in ngrams_dic.values(): #sommation
        sommation += value/total * math.log(value/total, 2)
    sommation = sommation / (k+1)
    return -sommation

def functional_load(words_dic, phon1, phon2):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param phon1: phoneme replaced
    :param phon2: phoneme used as replacement
    :return: the different in entropy between the two states
    '''
    merged_words = Counter()
    for word in words_dic:
        merged_words[word.replace(phon1, phon2)] += words_dic[word]
    print(round((entropy(words_dic)-entropy(merged_words))/entropy(words_dic), 4))

'''
This prints the functional load for the pairs mentioned in the work
'''

#open vowels
functional_load(words_tokens, 'E', 'e')
functional_load(words_tokens, '9', '2')
functional_load(words_tokens, 'o', 'O')

functional_load(words_tokens, 'u', 'o')
functional_load(words_tokens, 'O', 'a')
functional_load(words_tokens, 'a', 'E')
functional_load(words_tokens, 'a', '9')
functional_load(words_tokens, '2', 'E')
functional_load(words_tokens, '9', 'E')
functional_load(words_tokens, '2', 'e')
functional_load(words_tokens, 'e', 'i')
functional_load(words_tokens, 'y', 'e')
functional_load(words_tokens, 'y', 'i')


#nasals
functional_load(words_tokens, '5', '1')
functional_load(words_tokens, '§', '1')
functional_load(words_tokens, '@', '1')
